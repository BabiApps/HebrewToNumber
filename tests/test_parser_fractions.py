import pytest
from app.parser import hebrew_to_number

@pytest.mark.fractions
@pytest.mark.parametrize("text,expected", [
    ("חצי", 0.5),
    ("רבע", 0.25),
    ("מיליון וחצי", 1_500_000.0),
    ("מיליון ו חצי", 1_500_000.0),
    ("מיליון ורבע", 1_250_000.0),
    ("5 ורבע מיליון", 5_250_000.0),
    ("חמש מאות וחצי", 500.5),
    ("חמש מאות ו רבע", 500.25),
    ("אלף שלוש וחצי", 1003.5),
])
def test_fractions(text, expected):
    assert hebrew_to_number(text) == expected

@pytest.mark.strict
@pytest.mark.parametrize("text", [
    "חצי חצי",
    "וחצי חצי",
    "אחד ורבע וחצי",
    "אחד וחצי ורבע",
])
def test_fraction_strictness(text):
    import pytest
    with pytest.raises(ValueError):
        hebrew_to_number(text)
