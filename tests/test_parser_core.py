import pytest
from app.parser import hebrew_to_number

@pytest.mark.parametrize("text,expected", [
    ("ואחת", 1),
    ("3 אלפים", 3000),
    ("12 אלפים", 12000),
    ("תשע מאות תשעים ותשע מיליון תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע", 999_999_999),
])
def test_core_numbers(text, expected):
    assert hebrew_to_number(text) == expected
