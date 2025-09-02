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
    "עשרים": 20,
    "שלושים": 30,
    "ארבעים": 40,
    "חמישים": 50,
    "שישים": 60,
    "שבעים": 70,
    "שמונים": 80,
    "תשעים": 90,
}

hebrew_hundreds = {
    "מאה": 100,
    "מאתיים": 200,
    "שלוש מאות": 300,
    "ארבע מאות": 400,
    "חמש מאות": 500,
    "שש מאות": 600,
    "שבע מאות": 700,
    "שמונה מאות": 800,
    "תשע מאות": 900,
}

multipliers = {
    "אלף": 1_000,
    "אלפיים": 2_000,
    "אלפים": 1_000,
    "מיליון": 1_000_000,
    "מליון": 1_000_000,
    "מיליארד": 1_000_000_000,
    "מליארד": 1_000_000_000,
}


def hebrew_to_number(text: str) -> float:
    """
    גרסה בטוחה של הפונקציה הממירה טקסט בעברית למספר עשרוני.
    מחזירה ValueError במקום לזרוק חריגה.
    """
    parts_raw = text.replace("־", " ").split()
    # keep flags whether a token started with 'ו' (e.g., 'וחצי')
    has_vav = [p.startswith("ו") and len(p) > 1 for p in parts_raw]
    parts = [p[1:] if hv else p for p, hv in zip(parts_raw, has_vav)]
    total = 0
    current = 0
    i = 0

    # keep track of last multiplier to check order
            # מאות כשתי מילים

    last_was_half = False
    groups = []
    current_group = 0
    i = 0
    while i < len(parts):
        word = parts[i]
        # special handling for standalone 'חצי'
        if word == "חצי":
            # if 'חצי' precedes a multiplier: 'חצי מיליון' => 0.5 * מיליון
            if i + 1 < len(parts) and parts[i + 1] in multipliers:
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                groups.append((0.5, multipliers[parts[i + 1]]))
                current_group = 0
                last_was_half = True
                i += 2
                continue
            # otherwise treat as 0.5 added to the current (fractional) part
            if last_was_half:
                raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
            current_group += 0.5
            last_was_half = True
            i += 1
            continue
        # מאות כשתי מילים
        if i + 1 < len(parts):
            two_words = f"{word} {parts[i+1]}"
            if two_words in hebrew_hundreds:
                # בדיקה אם "חצי" בא אחרי מאות
                if i + 2 < len(parts) and parts[i+2] == "חצי":
                    if last_was_half:
                        raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                    current_group += hebrew_hundreds[two_words] + 0.5
                    last_was_half = True
                    i += 3
                    continue
                current_group += hebrew_hundreds[two_words]
                last_was_half = False
                i += 2
                continue
        # מספרים עשרוניים
        if re.match(r"^\d+(\.\d+)?$", word):
            # בדיקה אם "חצי" בא אחרי מספר
            if i + 1 < len(parts) and parts[i + 1] == "חצי":
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                current_group += float(word) + 0.5
                last_was_half = True
                i += 2
                continue
            current_group += float(word)
            last_was_half = False
            i += 1
            continue
        # מאות
        if word in hebrew_hundreds:
            # בדיקה אם "חצי" בא אחרי מאות
            if i + 1 < len(parts) and parts[i+1] == "חצי":
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                current_group += hebrew_hundreds[word] + 0.5
                last_was_half = True
                i += 2
                continue
            current_group += hebrew_hundreds[word]
            last_was_half = False
            i += 1
            continue
        # עשרות
        if word in hebrew_tens:
            # בדיקה אם "חצי" בא אחרי עשרות
            if i + 1 < len(parts) and parts[i+1] == "חצי":
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                current_group += hebrew_tens[word] + 0.5
                last_was_half = True
                i += 2
                continue
            current_group += hebrew_tens[word]
            last_was_half = False
            i += 1
            continue
        # יחידות
        if word in hebrew_units:
            val = hebrew_units[word]
            # בדיקה אם "וחצי" בא אחרי מספר יחידות
            if i + 2 < len(parts) and parts[i + 1] == "ו" and parts[i + 2] == "חצי":
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                current_group += val + 0.5
                last_was_half = True
                i += 3
                continue
            elif i + 1 < len(parts) and parts[i + 1] == "חצי":
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                current_group += val + 0.5
                last_was_half = True
                i += 2
                continue
            else:
                current_group += val
                last_was_half = False
                i += 1
                continue
        # multipliers
        if word in multipliers:
            multiplier_value = multipliers[word]
            if groups and multiplier_value >= groups[-1][1]:
                raise ValueError(f"Unlogical multiplier word order: \ncurrent: {word} ({multiplier_value}), last: {groups[-1][1]}")
            # detect attached 'וחצי' or separated 'ו חצי'
            attached_half = False
            if i + 2 < len(parts) and parts[i + 1] == "ו" and parts[i + 2] == "חצי":
                attached_half = True
            elif i + 1 < len(parts) and has_vav[i + 1] and parts[i + 1] == "חצי":
                attached_half = True

            if attached_half:
                if last_was_half:
                    raise ValueError("לא ניתן להשתמש ב'חצי' פעמיים ברצף")
                # If a larger multiplier was already seen (e.g., מיליארד ... מיליון וחצי)
                # the trailing 'וחצי' is treated as half a unit (0.5), not half of the smaller multiplier.
                larger_before = bool(groups and groups[-1][1] > multiplier_value)
                if current_group == 0:
                    if larger_before:
                        groups.append((1, multiplier_value))
                        groups.append((0.5, 1))
                    else:
                        groups.append((1.5, multiplier_value))
                else:
                    if larger_before:
                        groups.append((current_group, multiplier_value))
                        groups.append((0.5, 1))
                    else:
                        groups.append((current_group + 0.5, multiplier_value))
                current_group = 0
                last_was_half = True
                i += 2 if parts[i + 1] == "ו" else 2
                continue

            # normal attached multiplier
            if current_group == 0:
                groups.append((1, multiplier_value))
                current_group = 0
                last_was_half = False
                i += 1
                continue
            else:
                groups.append((current_group, multiplier_value))
                current_group = 0
                last_was_half = False
                i += 1
                continue
        # ביטויים כפולי מילים (multipliers)
        if i + 1 < len(parts):
            two_words = f"{word} {parts[i+1]}"
            if two_words in multipliers:
                multiplier_value = multipliers[two_words]
                if groups and multiplier_value >= groups[-1][1]:
                    raise ValueError(f"סדר מילים לא הגיוני: {two_words}")
                if current_group == 0:
                    current_group = 1
                groups.append((current_group, multiplier_value))
                current_group = 0
                last_was_half = False
                i += 2
                continue
        raise ValueError(f"מילה לא מוכרת: {word}")

    # סכימה סופית
    total = 0
    for group, multiplier in groups:
        total += group * multiplier
    total += current_group
    return total
