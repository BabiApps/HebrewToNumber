from parser import hebrew_to_number

# Categorized tests for clarity — each category prints its own header and results
grouped_valid = [
    ("Basic numbers", [
        ("אפס", 0),
        ("אחת עשרה", 11),
        ("שש עשרה", 16),
        ("מאה עשרים ושלוש", 123),
        ("מאתיים חמישים ושבע", 257),
        ("אלף מאתיים שלושים וארבע", 1234),
        ("תשע מאות תשעים ותשע", 999),
        ("ארבע מאות חמישים ושבע", 457),
        ("עשר אלף", 10_000),
    ]),

    ("Hundreds / Thousands / Millions", [
        ("אלף אפס", 1_000),
        ("מיליון", 1_000_000),
        ("שני מיליון", 2_000_000),
        ("מיליון ומאתיים שלושים אלף", 1_230_000),
        ("שלוש מאות אלף שש מאות ושבעים", 300_670),
        ("ארבעה מיליארד שלוש מאות מיליון", 4_300_000_000),
        ("תשע מאות אלף תשע מאות תשעים ותשע", 900_999),
        ("מיליון אחת", 1_000_001),
    ]),

    ("Composed complex numbers", [
        ("שלושה מיליון מאתיים אלף", 3_200_000),
        ("חמישה מיליון מאה אלף", 5_100_000),
        ("מיליארד ושבע מאות אלף שלוש מאות תשעים ואחד", 1_000_700_391),
        ("שבע מאות שמונים ותשע אלף מאתיים שלושים ואחד", 789_231),
        ("מיליארד מיליון אלף", 1_001_001_000),
    ]),

    ("Fractions & halves", [
        ("חצי מיליון", 500_000),
        ("מיליון וחצי", 1_500_000),
        ("מיליון וחצי 3 אלף וחמש מאות 30", 1_503_530),
        ("שני מיליון וחצי", 2_500_000),
        ("אלף שלוש וחצי", 1_003.5),
        ("מאה אלף חצי", 100_000.5),
        ("חצי", 0.5),
        ("אחד וחצי", 1.5),
    ]),

    ("Decimals mixed with words", [
        ("67 אלף", 67_000.0),
        ("10.3 מיליון", 10_300_000.0),
        ("2.5 מיליארד", 2_500_000_000.0),
        ("0.5 מיליון", 500_000.0),
        ("3.1415 מיליון", 3_141_500.0),
    ]),

    ("Vav prefixes (ו-) and hyphenation", [
        ("ועשרים", 20),
        ("ושש מאות", 600),
        ("וחמישה מיליון", 5_000_000),
        ("עשרים־שלושה אלף", 23_000),
        ("עשרים־שלושה אלף ארבע מאות", 23_400),
    ]),

    ("Edge / large boundaries", [
        ("תשע מאות תשעים ותשע מיליון תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע", 999_999_999),
        ("תשע מאות תשעים ותשע מיליארד תשע מאות תשעים ותשע מיליון תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע", 999_999_999_999),
    ]),
]

grouped_invalid = [
    ("Ambiguous / ordering errors", [
        "2 מליון ומיליון וחצי",
        "מליון מיליון",
        "אלף מיליון",
        "שלוש מאות מיליון מיליון",
        "חמש אלף אלף",
        "שלוש אלף אלף",
        "מיליון מיליון מיליון",
        "אלף אלף אלף",
        "מיליון שלוש מיליון",
        "מיליארד מיליארד",
        "אלף שלוש מאות אלף",
        "מיליון שלוש מאות מיליון מיליון",
    ]),
    ("Double halves / invalid half usage", [
        "חצי מיליון חצי",
        "שלוש חצי חצי",
        "חצי חצי",
        "מיליון חצי חצי",
    ]),
]


def run_group(name, tests):
    print(f"\n=== {name} ===")
    for case, expected in tests:
        try:
            result = hebrew_to_number(case)
            if isinstance(expected, type) and issubclass(expected, Exception):
                print(f"❌ Test failed (should raise) '{case}' => {result}")
            else:
                if result == expected:
                    print(f"✅ '{case}' => {result}")
                else:
                    print(f"❌ '{case}' => {result}, expected {expected}")
        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, Exception):
                print(f"✅ '{case}' => correctly raised {e}")
            else:
                print(f"❌ Exception for '{case}': {e}")


def run_invalid_group(name, tests):
    print(f"\n--- {name} (should raise ValueError) ---")
    for text in tests:
        try:
            result = hebrew_to_number(text)
            print(f"❌ Test failed (should throw error) '{text}' => {result}")
        except ValueError as e:
            print(f"✅ '{text}' => correctly raised ValueError: {e}")


if __name__ == '__main__':
    print("🔵 Categorized Valid Tests")
    for name, tests in grouped_valid:
        run_group(name, tests)

    print("\n🟠 Categorized Invalid Tests")
    for name, tests in grouped_invalid:
        run_invalid_group(name, tests)


# --- Challenging grouped tests ---
groups = [
    ("Vav prefixes (ו-)", [
        ("ועשרים", 20),
        ("ושש מאות", 600),
        ("וחמישה מיליון", 5_000_000),
    ]),

    ("Fractions and halves",
     [
         ("חצי", 0.5),
         ("אחד וחצי", 1.5),
         ("שלוש וחצי מיליון", 3_500_000),
         ("שש מאות חצי", 600.5),
     ]),

    ("Decimal numerals mixed with words", [
        ("0.5 מיליון", 500_000.0),
        ("3.1415 מיליון", 3_141_500.0),
        ("0.25 מיליון", 250_000.0),
    ]),

    ("Hyphenation and dashes", [
        ("עשרים־שלושה אלף", 23_000),
        ("עשרים־שלושה אלף ארבע מאות", 23_400),
    ]),

    ("Ambiguous / ordering issues (should raise)", [
        ("מיליון אלף מיליון", ValueError),
        ("חצי חצי", ValueError),
        ("מיליון חצי חצי", ValueError),
    ]),

    ("Edge large / boundary cases", [
        ("תשע מאות תשעים ותשע מיליארד תשע מאות תשעים ותשע מיליון תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע",
         999_999_999_999),
    ]),
]


def run_group(name, tests):
    print(f"\n=== {name} ===")
    for case, expected in tests:
        try:
            result = hebrew_to_number(case)
            if isinstance(expected, type) and issubclass(expected, Exception):
                print(f"❌ Test failed (should raise) '{case}' => {result}")
            else:
                if result == expected:
                    print(f"✅ '{case}' => {result}")
                else:
                    print(f"❌ '{case}' => {result}, expected {expected}")
        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, Exception):
                print(f"✅ '{case}' => correctly raised {e}")
            else:
                print(f"❌ Exception for '{case}': {e}")


print("\n🔎 Additional grouped challenging tests")
for name, tests in groups:
    run_group(name, tests)
