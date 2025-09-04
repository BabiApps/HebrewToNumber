import pytest
from app.parser import hebrew_to_number

@pytest.mark.decimals
@pytest.mark.parametrize("text,expected", [
    ("נקודה שבע", 0.7),
    ("נקודה אפס שבע", 0.07),
    ("נקודה שבע אלף", 0.7000),
    ("אפס נקודה שבע אלף", 0.7000),
    ("שלוש נקודה ארבע", 3.4),
    ("ארבע נקודה 2 5", 4.25),
    ("אפס נקודה שבע מאות ושבע", 0.707),
    ("אפס נקודה תשע מאות תשעים ותשע", 0.999),
    ("עשר נקודה אפס אפס אפס חמש", 10.0005),
    ("עשרים נקודה עשרים", 20.20),
    ("שתיים נקודה חמש מיליון", 2_500_000.0),
    ("חמישים ושש נקודה שבע אלף", 56.7000),
])
def test_decimals(text, expected):
    assert hebrew_to_number(text) == expected

@pytest.mark.strict
@pytest.mark.parametrize("text", [
    "חמש נקודה מיליון",
])
def test_decimals_invalid(text):
    import pytest
    with pytest.raises(ValueError):
        hebrew_to_number(text)
