import pytest
from app.parser import hebrew_to_number

@pytest.mark.strict
@pytest.mark.parametrize("text", [
    "2 מיליון ומיליון וחצי",
    "מיליון מיליון",
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
])
def test_invalid_repeated_or_ascending_scales(text):
    with pytest.raises(ValueError):
        hebrew_to_number(text)
