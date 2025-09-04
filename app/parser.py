import re

hebrew_units = {
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
}
hebrew_tens = {
    "עשר": 10, "עשרה": 10,
    "עשרים": 20, "שלשים": 30, "שלושים": 30,
    "ארבעים": 40, "חמישים": 50, "שישים": 60,
    "שבעים": 70, "שמונים": 80, "תשעים": 90,
}
hebrew_hundreds = {
    "מאה": 100, "מאתיים": 200, "מאתים": 200,
    "שלוש מאות": 300, "שלושה מאות": 300,
    "ארבע מאות": 400,
    "חמש מאות": 500,
    "שש מאות": 600,
    "שבע מאות": 700,
    "שמונה מאות": 800,
    "תשע מאות": 900,
}
scales = {"אלף": 1000, "אלפים": 1000, "מיליון": 1_000_000, "מליון": 1_000_000, "מיליארד": 1_000_000_000, "מליארד": 1_000_000_000}
fractions_map = {"חצי": 0.5, "רבע": 0.25}

def _is_number_token(tok: str) -> bool:
    return bool(re.fullmatch(r"\d+(?:\.\d+)?", tok))

def _tokenize(text: str):
    parts_raw = text.replace("־", " ").split()
    has_vav = [p.startswith("ו") and len(p) > 1 for p in parts_raw]
    parts = [p[1:] if hv else p for p, hv in zip(parts_raw, has_vav)]
    # normalize "אלפיים" -> "שניים אלפים"
    normalized = []
    vflags = []
    for tok, hv in zip(parts, has_vav):
        if tok == "אלפיים":
            normalized.extend(["שניים", "אלפים"])
            vflags.extend([False, False])
        else:
            normalized.append(tok); vflags.append(hv)
    return normalized, vflags

def _parse_decimal_phrase(tokens):
    """Parse tokens after 'נקודה' into digits string according to rules:
       - supports digits, units, tens, hundreds (including two-word 'X מאות'), and אלף/אלפים.
       - phrase is interpreted as an integer, then used as fractional digits: 0.<digits>"""
    # detect magnitudes
    has_magnitude = False
    for i, t in enumerate(tokens):
        if t in hebrew_tens or t in hebrew_hundreds or t in ("אלף", "אלפים"):
            has_magnitude = True; break
        if i + 1 < len(tokens) and f"{t} {tokens[i+1]}" in hebrew_hundreds:
            has_magnitude = True; break
    # compute integer value
    val = 0
    group = 0
    k = 0
    while k < len(tokens):
        t = tokens[k]
        if k + 1 < len(tokens) and f"{t} {tokens[k+1]}" in hebrew_hundreds:
            group += hebrew_hundreds[f"{t} {tokens[k+1]}"]
            k += 2; continue
        if t in hebrew_hundreds:
            group += hebrew_hundreds[t]; k += 1; continue
        if t in hebrew_tens:
            group += hebrew_tens[t]; k += 1; continue
        if t in hebrew_units:
            group += hebrew_units[t]; k += 1; continue
        if re.fullmatch(r"\d+", t):
            group = group * (10 ** len(t)) + int(t); k += 1; continue
        if t in ("אלף", "אלפים"):
            if group == 0:
                group = 1
            val = val * 1000 + group * 1000
            group = 0
            k += 1; continue
        break
    val += group
    digits = str(int(val)) if val > 0 else "0"
    if not has_magnitude:
        # preserve explicit leading zeros
        lead_zeros = 0
        for t in tokens:
            if t == "אפס" or re.fullmatch(r"0+", t):
                lead_zeros += 1
            else:
                break
        if lead_zeros:
            digits = "0" * lead_zeros + (str(int(val)) if val > 0 else "0")
    return digits

def hebrew_to_number(text: str) -> float:
    parts, has_vav = _tokenize(text)
    i = 0
    groups = []  # list of (value, multiplier)
    current_group = 0.0
    used_fraction = False
    seen_tens_in_segment = False  # reset on scales
    last_scale_value = None

    # strictness pre-checks
    for idx in range(len(parts) - 1):
        # two tens in same contiguous segment (without hitting scale)
        if parts[idx] in hebrew_tens:
            j = idx + 1
            if j < len(parts) and parts[j] == "ו":
                j += 1
            if j < len(parts) and parts[j] in hebrew_tens:
                raise ValueError("ניסוח לא תקין: שתי עשרות ברצף באותו מספר. נסי לנסח מחדש (למשל: 'אלף מאה וחמישים' במקום 'אלף שמונים שבעים').")
        # 'חמישים אלפיים' style
        if parts[idx] in hebrew_tens and (parts[idx+1] == "אלפיים" or (idx+2 < len(parts) and parts[idx+1] in ("שניים","שתיים","שני") and parts[idx+2] == "אלפים")):
            raise ValueError("ניסוח לא תקין: 'חמישים אלפיים' אינו תקין. כתבי 'חמישים אלף' או 'חמישים ושניים אלף'.")

    while i < len(parts):
        w = parts[i]

        # decimal point
        if w == "נקודה":
            j = i + 1
            allowed = []
            while j < len(parts):
                t = parts[j]
                if t == "ו": break
                if t in ("מיליון", "מליון", "מיליארד", "מליארד"): break
                # two-word hundreds
                if j + 1 < len(parts) and f"{t} {parts[j+1]}" in hebrew_hundreds:
                    allowed.append(t); allowed.append(parts[j+1]); j += 2; continue
                if re.fullmatch(r"\d+", t) or t in hebrew_units or t in hebrew_tens or t in hebrew_hundreds or t in ("אלף","אלפים"):
                    allowed.append(t); j += 1; continue
                break
            if not allowed:
                raise ValueError("ניסוח לא תקין: אחרי 'נקודה' חייב לבוא ביטוי מספרי (למשל: 'נקודה חמש' / 'נקודה שבע מאות').")
            digits = _parse_decimal_phrase(allowed)
            current_group += float("0." + digits)
            i = j
            continue

        # separate 'ו חצי' / 'ו רבע'
        if w == "ו" and i + 1 < len(parts) and parts[i+1] in fractions_map:
            if used_fraction:
                raise ValueError("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי")
            frac = fractions_map[parts[i+1]]
            if current_group > 0:
                current_group += frac
            elif groups:
                # attach to last scale
                last_mult = groups[-1][1]
                groups.append((frac, last_mult))
            else:
                current_group += frac
            used_fraction = True
            i += 2
            continue

        # standalone 'חצי' / 'רבע'
        if w in fractions_map:
            if used_fraction:
                raise ValueError("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי")
            current_group += fractions_map[w]
            used_fraction = True
            i += 1
            continue

        # numeric token
        if _is_number_token(w):
            num = float(w)
            # optionally followed by 'ו חצי/חצי' etc.
            if i + 2 < len(parts) and parts[i+1] == "ו" and parts[i+2] in fractions_map and not used_fraction:
                num += fractions_map[parts[i+2]]
                used_fraction = True
                i += 3
            elif i + 1 < len(parts) and parts[i+1] in fractions_map and not used_fraction:
                num += fractions_map[parts[i+1]]
                used_fraction = True
                i += 2
            else:
                i += 1
            current_group += num
            seen_tens_in_segment = False
            continue

        # two-word hundreds
        if i + 1 < len(parts) and f"{w} {parts[i+1]}" in hebrew_hundreds:
            current_group += hebrew_hundreds[f"{w} {parts[i+1]}"]
            i += 2
            seen_tens_in_segment = False
            continue

        # single-word hundreds
        if w in hebrew_hundreds:
            current_group += hebrew_hundreds[w]
            i += 1
            seen_tens_in_segment = False
            continue

        # tens
        if w in hebrew_tens:
            if seen_tens_in_segment:
                raise ValueError("ניסוח לא תקין: שתי עשרות ברצף באותו מספר. נסי לנסח מחדש (למשל: 'אלף מאה וחמישים' במקום 'אלף שמונים שבעים').")
            current_group += hebrew_tens[w]
            i += 1
            seen_tens_in_segment = True
            continue

        # units
        if w in hebrew_units:
            current_group += hebrew_units[w]
            i += 1
            continue

        # scales
        if w in scales:
            mult = scales[w]
            # enforce descending order of scales: once a scale is used, following scales must be strictly smaller
            if last_scale_value is not None and mult >= last_scale_value:
                raise ValueError("ניסוח לא תקין: לא ניתן להשתמש בשני מכפילים מאותו סדר גודל או גדול יותר ברצף (למשל 'מיליון מיליון', 'אלף מיליון').")
            last_scale_value = mult
            group_val = current_group if current_group != 0 else 1
            groups.append((group_val, mult))
            current_group = 0.0
            seen_tens_in_segment = False

            # attached 'ו' fraction after scale (e.g., 'מיליון וחצי' or 'מיליון ו חצי')
            if i + 2 < len(parts) and parts[i+1] == "ו" and parts[i+2] in fractions_map:
                if used_fraction:
                    raise ValueError("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי")
                groups.append((fractions_map[parts[i+2]], mult))
                used_fraction = True
                i += 3
                continue
            if i + 1 < len(parts) and has_vav[i+1] and parts[i+1] in fractions_map:
                if used_fraction:
                    raise ValueError("לא ניתן להשתמש בתוספת שבר (חצי/רבע) יותר מפעם אחת בביטוי")
                groups.append((fractions_map[parts[i+1]], mult))
                used_fraction = True
                i += 2
                continue

            i += 1
            continue

        raise ValueError(f"מילה לא מוכרת: {w}")

    total = sum(g*m for g, m in groups) + current_group
    return total
