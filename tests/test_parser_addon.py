import pytest
from app.parser import hebrew_to_number


# --- Basic numbers ---
@pytest.mark.parametrize("text,expected", [
    ("אפס", 0),
    ("אחת עשרה", 11),
    ("שש עשרה", 16),
    ("מאה עשרים ושלוש", 123),
    ("מאתיים חמישים ושבע", 257),
    ("אלף מאתיים שלושים וארבע", 1234),
    ("תשע מאות תשעים ותשע", 999),
    ("ארבע מאות חמישים ושבע", 457),
    ("עשר אלף", 10_000),
])
def test_basic_numbers(text, expected):
    assert hebrew_to_number(text) == expected


# --- Hundreds / Thousands / Millions ---
@pytest.mark.parametrize("text,expected", [
    ("אלף אפס", 1_000),
    ("מיליון", 1_000_000),
    ("שני מיליון", 2_000_000),
    ("מיליון ומאתיים שלושים אלף", 1_230_000),
    ("שלוש מאות אלף שש מאות ושבעים", 300_670),
    ("ארבעה מיליארד שלוש מאות מיליון", 4_300_000_000),
    ("תשע מאות אלף תשע מאות תשעים ותשע", 900_999),
    ("מיליון אחת", 1_000_001),
])
def test_hundreds_thousands_millions(text, expected):
    assert hebrew_to_number(text) == expected


# --- Composed complex numbers ---
@pytest.mark.parametrize("text,expected", [
    ("שלושה מיליון מאתיים אלף", 3_200_000),
    ("חמישה מיליון מאה אלף", 5_100_000),
    ("מיליארד ושבע מאות אלף שלוש מאות תשעים ואחד", 1_000_700_391),
    ("שבע מאות שמונים ותשע אלף מאתיים שלושים ואחד", 789_231),
    ("מיליארד מיליון אלף", 1_001_001_000),
])
def test_composed_complex_numbers(text, expected):
    assert hebrew_to_number(text) == expected


# --- Fractions & halves ---
@pytest.mark.parametrize("text,expected", [
    ("חצי מיליון", 500_000),
    ("מיליון וחצי", 1_500_000),
    ("מיליון וחצי 3 אלף וחמש מאות 30", 1_503_530),
    ("שני מיליון וחצי", 2_500_000),
    ("אלף שלוש וחצי", 1_003.5),
    ("מאה אלף חצי", 100_000.5),
    ("חצי", 0.5),
    ("אחד וחצי", 1.5),
])
def test_fractions_and_halves(text, expected):
    assert hebrew_to_number(text) == expected


# --- Decimals mixed with words ---
@pytest.mark.parametrize("text,expected", [
    ("67 אלף", 67_000.0),
    ("10.3 מיליון", 10_300_000.0),
    ("2.5 מיליארד", 2_500_000_000.0),
    ("0.5 מיליון", 500_000.0),
    ("3.1415 מיליון", 3_141_500.0),
])
def test_decimals_with_words(text, expected):
    assert hebrew_to_number(text) == expected


# --- Vav prefixes and hyphenation ---
@pytest.mark.parametrize("text,expected", [
    ("ועשרים", 20),
    ("ושש מאות", 600),
    ("וחמישה מיליון", 5_000_000),
    ("עשרים־שלושה אלף", 23_000),
    ("עשרים־שלושה אלף ארבע מאות", 23_400),
])
def test_vav_and_hyphenation(text, expected):
    assert hebrew_to_number(text) == expected


# --- Edge / large boundaries ---
@pytest.mark.parametrize("text,expected", [
    ("תשע מאות תשעים ותשע מיליון תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע",
     999_999_999),
    ("תשע מאות תשעים ותשע מיליארד תשע מאות תשעים ותשע מיליון "
     "תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע",
     999_999_999_999),
])
def test_large_boundaries(text, expected):
    assert hebrew_to_number(text) == expected


# --- Invalid numbers (should raise ValueError) ---
@pytest.mark.parametrize("text", [
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
    "חצי מיליון חצי",
    "שלוש חצי חצי",
    "חצי חצי",
    "מיליון חצי חצי",
])
def test_invalid_numbers_raise_value_error(text):
    with pytest.raises(ValueError):
        hebrew_to_number(text)


# --- Additional challenging grouped tests ---
@pytest.mark.parametrize("text,expected", [
    ("ועשרים", 20),
    ("ושש מאות", 600),
    ("וחמישה מיליון", 5_000_000),
    ("חצי", 0.5),
    ("אחד וחצי", 1.5),
    ("שלוש וחצי מיליון", 3_500_000),
    ("שש מאות חצי", 600.5),
    ("0.5 מיליון", 500_000.0),
    ("3.1415 מיליון", 3_141_500.0),
    ("0.25 מיליון", 250_000.0),
    ("עשרים־שלושה אלף", 23_000),
    ("עשרים־שלושה אלף ארבע מאות", 23_400),
    ("תשע מאות תשעים ותשע מיליארד תשע מאות תשעים ותשע מיליון "
     "תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע",
     999_999_999_999),
])
def test_additional_challenging_cases(text, expected):
    assert hebrew_to_number(text) == expected


@pytest.mark.parametrize("text", [
    "מיליון אלף מיליון",
    "חצי חצי",
    "מיליון חצי חצי",
])
def test_additional_invalid_cases(text):
    with pytest.raises(ValueError):
        hebrew_to_number(text)
