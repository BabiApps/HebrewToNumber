from app.parser import hebrew_units, hebrew_tens, hebrew_hundreds

def number_to_hebrew(num: float) -> str:
    """
    המרה בסיסית ממספר לעברית: חלק שלם עד מיליארדים, וחלק עשרוני כספרות אחרי 'נקודה'.
    נועדה כבסיס — לא מכסה דקדוק מלא (שני/שלושה/שלושת אלפים...), אך שימושית לבדיקות.
    """
    import math
    def units_word(x):
        for k, v in hebrew_units.items():
            if v == x and k not in ("שניים", "שתיים", "שני", "אחת"):
                return k
        return "אפס"
    def tens_word(x):
        for k, v in hebrew_tens.items():
            if v == x:
                return k
        return ""
    def hundreds_word(x):
        for k, v in hebrew_hundreds.items():
            if v == x:
                return k
        return ""

    whole = int(math.floor(abs(num)))
    words = []
    def push_group(amount, label):
        if amount == 0: return
        if amount == 1: words.append(label); return
        if amount < 10: words.append(units_word(amount))
        elif amount < 100 and amount % 10 == 0: words.append(tens_word(amount))
        elif amount < 1000 and amount % 100 == 0: words.append(hundreds_word(amount))
        else: words.append(str(amount))
        words.append(label)

    billions, rem = divmod(whole, 1_000_000_000)
    millions, rem = divmod(rem, 1_000_000)
    thousands, rest = divmod(rem, 1000)

    push_group(billions, "מיליארד")
    push_group(millions, "מיליון")
    if thousands:
        if thousands == 1: words.append("אלף")
        else: words += [str(thousands), "אלף"]

    if rest >= 100:
        h = (rest // 100) * 100; words.append(hundreds_word(h)); rest -= h
    if rest >= 10:
        t = (rest // 10) * 10; words.append(tens_word(t)); rest -= t
    if rest > 0:
        words.append(units_word(rest))

    frac = abs(num) - int(abs(num))
    if frac > 0:
        digits = str(frac).split(".")[1].rstrip("0")
        if digits:
            digit_words = [units_word(int(d)) for d in digits]
            words += ["נקודה"] + digit_words

    if num < 0: words.insert(0, "מינוס")
    return " ".join([w for w in words if w])
