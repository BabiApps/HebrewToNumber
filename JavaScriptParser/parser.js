const hebrewUnits = new Map(Object.entries({
  "אפס": 0,
  "אחת": 1, "אחד": 1,
  "שתיים": 2, "שניים": 2, "שתי": 2, "שני": 2,
  "שלוש": 3, "שלושה": 3,
  "ארבע": 4, "ארבעה": 4,
  "חמש": 5, "חמישה": 5,
  "שש": 6, "שישה": 6,
  "שבע": 7, "שבעה": 7,
  "שמונה": 8,
  "תשע": 9, "תשעה": 9,
}));

const hebrewTens = new Map(Object.entries({
  "עשר": 10, "עשרה": 10,
  "עשרים": 20, "שלשים": 30, "שלושים": 30,
  "ארבעים": 40, "חמישים": 50, "שישים": 60,
  "שבעים": 70, "שמונים": 80, "תשעים": 90,
}));

const hebrewHundreds = new Map(Object.entries({
  "מאה": 100, "מאתיים": 200, "מאתים": 200,
  "שלוש מאות": 300, "שלושה מאות": 300,
  "ארבע מאות": 400,
  "חמש מאות": 500,
  "שש מאות": 600,
  "שבע מאות": 700,
  "שמונה מאות": 800,
  "תשע מאות": 900,
}));

const scales = new Map(Object.entries({
  "אלף": 1000, "אלפים": 1000,
  "מיליון": 1000000, "מליון": 1000000,
  "מיליארד": 1000000000, "מליארד": 1000000000,
}));

function isNumberToken(tok) { return /^\d+(?:\.\d+)?$/.test(tok); }

function tokenize(text) {
  // split by whitespace; keep dots if attached (will be invalid)
  const raw = text.replace(/־/g, " ").trim().split(/\s+/).filter(Boolean);
  const hasVav = raw.map(p => p.startsWith("ו") && p.length > 1);
  const parts = raw.map((p, i) => hasVav[i] ? p.slice(1) : p);
  // normalize 'אלפיים' -> 'שניים אלפים'
  const normalized = [];
  const vflags = [];
  for (let i = 0; i < parts.length; i++) {
    const tok = parts[i], hv = hasVav[i];
    if (tok === "אלפיים") {
      normalized.push("שניים", "אלפים");
      vflags.push(false, false);
    } else {
      normalized.push(tok);
      vflags.push(hv);
    }
  }
  return { parts: normalized, hasVav: vflags };
}

function parseDecimalPhrase(tokens) {
  // Decide mode: digit-sequence (no magnitudes) vs numeric-phrase (with tens/hundreds/אלף)
  let hasMagnitude = false;
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    if (hebrewTens.has(t) || hebrewHundreds.has(t) || t === "אלף" || t === "אלפים") { hasMagnitude = true; break; }
    if (i + 1 < tokens.length && hebrewHundreds.has(`${t} ${tokens[i+1]}`)) { hasMagnitude = true; break; }
  }

  if (!hasMagnitude) {
    // Treat as a sequence of digits: units words -> single digits; numeric strings append as-is.
    let digits = "";
    for (let k = 0; k < tokens.length; k++) {
      const t = tokens[k];
      if (/^\d+$/.test(t)) { digits += t; continue; }
      if (hebrewUnits.has(t)) { digits += String(hebrewUnits.get(t)); continue; }
      // unknown token in digit mode -> stop
      break;
    }
    if (digits.length === 0) digits = "0";
    return digits;
  }

  // Numeric-phrase mode: compute an integer from tens/hundreds/אלף
  let val = 0, group = 0, k = 0;
  while (k < tokens.length) {
    const t = tokens[k];
    if (k + 1 < tokens.length && hebrewHundreds.has(`${t} ${tokens[k+1]}`)) { group += hebrewHundreds.get(`${t} ${tokens[k+1]}`); k += 2; continue; }
    if (hebrewHundreds.has(t)) { group += hebrewHundreds.get(t); k++; continue; }
    if (hebrewTens.has(t)) { group += hebrewTens.get(t); k++; continue; }
    if (hebrewUnits.has(t)) { group += hebrewUnits.get(t); k++; continue; }
    if (/^\d+$/.test(t)) { group = group * (10 ** t.length) + parseInt(t, 10); k++; continue; }
    if (t === "אלף" || t === "אלפים") {
      if (group === 0) group = 1;
      val = val * 1000 + group * 1000;
      group = 0;
      k++; continue;
    }
    break;
  }
  val += group;
  return val > 0 ? String(val) : "0";
}

export function hebrewToNumber(text) {
  const { parts, hasVav } = tokenize(text);
  let i = 0;
  const groups = [];
  let currentGroup = 0.0;
  let usedFraction = false;
  let seenTensInSegment = false;
  let seenUnitsInSegment = false;
  let usedDecimal = false;
  let lastScaleValue = null;

  // quick invalid tokens: trailing '.' etc.
  for (const w of parts) {
    if (/[.]/.test(w)) {
      // dots are only allowed inside plain digit tokens via isNumberToken, not appended to words
      if (!isNumberToken(w)) throw new Error("ניסוח לא תקין: נקודה לא במיקום תקין");
    }
  }

  // strictness pre-checks
  for (let idx = 0; idx < parts.length - 1; idx++) {
    if (hebrewTens.has(parts[idx])) {
      let j = idx + 1;
      if (parts[j] === "ו") j++;
      if (j < parts.length && hebrewTens.has(parts[j])) {
        throw new Error("ניסוח לא תקין: שתי עשרות ברצף באותו מספר.");
      }
    }
    if (hebrewTens.has(parts[idx]) && (parts[idx+1] === "אלפיים" || (idx+2 < parts.length && (parts[idx+1] === "שניים" || parts[idx+1] === "שתיים" || parts[idx+1] === "שני") && parts[idx+2] === "אלפים"))) {
      throw new Error("ניסוח לא תקין: 'חמישים אלפיים' אינו תקין.");
    }
  }

  while (i < parts.length) {
    const w = parts[i];

    if (w === "נקודה") {
      if (usedDecimal) throw new Error("ניסוח לא תקין: יותר מנקודה עשרונית אחת");
      let j = i + 1;
      const allowed = [];
      while (j < parts.length) {
        const t = parts[j];
        if (t === "ו") break;
        if (t === "מיליון" || t === "מליון" || t === "מיליארד" || t === "מליארד") break;
        if (j + 1 < parts.length && hebrewHundreds.has(`${t} ${parts[j+1]}`)) { allowed.push(t, parts[j+1]); j += 2; continue; }
        if (/^\d+$/.test(t) || hebrewUnits.has(t) || hebrewTens.has(t) || hebrewHundreds.has(t) || t === "אלף" || t === "אלפים") { allowed.push(t); j++; continue; }
        break;
      }
      if (!allowed.length) throw new Error("ניסוח לא תקין: אחרי 'נקודה' חייב לבוא ביטוי מספרי.");
      const digits = parseDecimalPhrase(allowed);
      currentGroup += Number("0." + digits);
      usedDecimal = true;
      i = j;
      continue;
    }

    if (w === "ו" && i + 1 < parts.length && (parts[i+1] === "חצי" || parts[i+1] === "רבע")) {
      if (usedFraction) throw new Error("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי");
      const frac = parts[i+1] === "חצי" ? 0.5 : 0.25;
      if (currentGroup > 0) currentGroup += frac;
      else if (groups.length) { const lastMult = groups[groups.length - 1][1]; groups.push([frac, lastMult]); }
      else currentGroup += frac;
      usedFraction = true;
      i += 2;
      continue;
    }

    if (parts[i] === "חצי" || parts[i] === "רבע") {
      if (usedFraction) throw new Error("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי");
      currentGroup += parts[i] === "חצי" ? 0.5 : 0.25;
      usedFraction = true;
      i += 1;
      continue;
    }

    if (isNumberToken(w)) {
      let num = parseFloat(w);
      if (i + 2 < parts.length && parts[i+1] === "ו" && (parts[i+2] === "חצי" || parts[i+2] === "רבע") && !usedFraction) {
        num += (parts[i+2] === "חצי" ? 0.5 : 0.25);
        usedFraction = true;
        i += 3;
      } else if (i + 1 < parts.length && (parts[i+1] === "חצי" || parts[i+1] === "רבע") && !usedFraction) {
        num += (parts[i+1] === "חצי" ? 0.5 : 0.25);
        usedFraction = true;
        i += 2;
      } else {
        i += 1;
      }
      currentGroup += num;
      seenTensInSegment = false;
      // numbers reset units/tens tracking for the segment
      seenUnitsInSegment = false;
      continue;
    }

    if (i + 1 < parts.length && hebrewHundreds.has(`${w} ${parts[i+1]}`)) {
      currentGroup += hebrewHundreds.get(`${w} ${parts[i+1]}`);
      i += 2;
      seenTensInSegment = false;
      // hundreds do not imply units yet
      continue;
    }

    if (hebrewHundreds.has(w)) {
      currentGroup += hebrewHundreds.get(w);
      i += 1;
      seenTensInSegment = false;
      continue;
    }

    if (hebrewTens.has(w)) {
      if (seenTensInSegment) throw new Error("ניסוח לא תקין: שתי עשרות ברצף באותו מספר.");
      currentGroup += hebrewTens.get(w);
      i += 1;
      seenTensInSegment = true;
      continue;
    }

    if (hebrewUnits.has(w)) {
      if (seenUnitsInSegment) throw new Error("ניסוח לא תקין: יותר מיחידת ספירה אחת באותו מקטע");
      currentGroup += hebrewUnits.get(w);
      i += 1;
      seenUnitsInSegment = true;
      continue;
    }

    if (scales.has(w)) {
      const mult = scales.get(w);
      if (lastScaleValue !== null && mult >= lastScaleValue) throw new Error("ניסוח לא תקין: לא ניתן להשתמש בשני מכפילים מאותו סדר גודל או גדול יותר ברצף.");
      lastScaleValue = mult;
      const groupVal = currentGroup !== 0 ? currentGroup : 1;
      groups.push([groupVal, mult]);
      currentGroup = 0.0;
      // reset segment flags
      seenTensInSegment = false;
      seenUnitsInSegment = false;
      usedDecimal = false; // decimal applies to the current small number only

      // attached 'ו' fraction after scale
      if (i + 2 < parts.length && parts[i+1] === "ו" && (parts[i+2] === "חצי" || parts[i+2] === "רבע")) {
        if (usedFraction) throw new Error("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי");
        groups.push([parts[i+2] === "חצי" ? 0.5 : 0.25, mult]);
        usedFraction = true; i += 3; continue;
      }
      if (i + 1 < parts.length && hasVav[i+1] && (parts[i+1] === "חצי" || parts[i+1] === "רבע")) {
        if (usedFraction) throw new Error("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי");
        groups.push([parts[i+1] === "חצי" ? 0.5 : 0.25, mult]);
        usedFraction = true; i += 2; continue;
      }

      i += 1;
      continue;
    }

    throw new Error(`מילה לא מוכרת: ${w}`);
  }

  let total = groups.reduce((s, [g,m]) => s + g*m, 0);
  total += currentGroup;
  return total;
}
