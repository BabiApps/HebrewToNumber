import pytest
from app.parser import hebrew_to_number

@pytest.mark.strict
@pytest.mark.parametrize("text", [
    "אלף שמונים שבעים",
    "מיליון ו",
    "חמישים אלפיים",
])
def test_strict_invalid(text):
    import pytest
    with pytest.raises(ValueError):
        hebrew_to_number(text)

@pytest.mark.parametrize("text,expected", [
    ("מיליון חמישים אלף חמש מאות", 1_050_500),
    ("אלף מאה וחמישים", 1_150),
])
def test_strict_valid_alternatives(text, expected):
    assert hebrew_to_number(text) == expected
