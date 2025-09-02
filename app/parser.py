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
    "חצי": 0.5,  # מילה מיוחדת
}

def hebrew_to_number(text: str) -> float:
    """
    גרסה בטוחה של הפונקציה הממירה טקסט בעברית למספר עשרוני.
    מחזירה ValueError במקום לזרוק חריגה.
    """
    parts = text.replace("־", " ").split()
    parts = [p[1:] if p.startswith("ו") and len(p) > 1 else p for p in parts]
    total = 0
    current = 0
    i = 0

    # keep track of last multiplier to check order
    last_multiplier_value = float('inf')  # מתחילים עם אינסוף כדי שכל multiplier יהיה קטן יותר

    while i < len(parts):
        word = parts[i]

        # מספרים עשרוניים
        if re.match(r"^\d+(\.\d+)?$", word):
            current += float(word)
            i += 1
            continue

        # ביטויים כפולי מילים
        if i + 1 < len(parts):
            two_words = f"{word} {parts[i+1]}"
            if two_words in hebrew_hundreds:
                current += hebrew_hundreds[two_words]
                i += 2
                continue
            if two_words in multipliers:
                multiplier_value = multipliers[two_words]
                if multiplier_value > last_multiplier_value:
                    raise ValueError(f"סדר מילים לא הגיוני: {two_words}")
                current = (current or 1) * multiplier_value
                total += current
                current = 0
                last_multiplier_value = multiplier_value
                i += 2
                continue

        # מאות
        if word in hebrew_hundreds:
            current += hebrew_hundreds[word]

        # עשרות
        elif word in hebrew_tens:
            current += hebrew_tens[word]

        # יחידות
        elif word in hebrew_units:
            current += hebrew_units[word]

        # מילים עם משקל גדול (אלף, מיליון, מיליארד, חצי)
        elif word in multipliers:
            multiplier_value = multipliers[word]

            # בדיקת סדר מילים
            if multiplier_value >= last_multiplier_value:
                raise ValueError(f"Unlogical multiplier word order: \ncurrent: {word} ({multiplier_value}), last: {last_multiplier_value}")

            # טיפול ב"חצי"
            if i + 1 < len(parts) and parts[i + 1] == "חצי":
                current = (current or 1) * multiplier_value * 1.5
                i += 1
            else:
                current = (current or 1) * multiplier_value

            total += current
            current = 0
            last_multiplier_value = multiplier_value

        else:
            raise ValueError(f"מילה לא מוכרת: {word}")

        i += 1

    total += current
    return total
