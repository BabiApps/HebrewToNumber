from fastapi import FastAPI
from pydantic import BaseModel
from .parser import hebrew_to_number

app = FastAPI(
    title="Hebrew Number Parser API",
    description="API to convert Hebrew text numbers to decimal integers",
    version="1.0.0"
)

class NumberRequest(BaseModel):
    text: str


@app.post("/hebrew-number")
def convert_number_post(req: NumberRequest):
    """
    מקבל טקסט בעברית ומחזיר את המספר העשרוני המתאים.\n
    דוגמה לבקשה:\n
    {
        "text": "אלף מאתיים שלושים וארבע"
    }\n
    דוגמה לתגובה:\n
    {
        "number": 1234
    }\n
    דוגמאות נוספות:\n
    - "אלפיים ושבע מאות וחמישים ושמונה"
    - "מיליון וחצי"
    - "2.5 מיליארד"
    """
    try:
        result = hebrew_to_number(req.text)
        return {"number": result}
    except ValueError as e:
        return {"error": str(e)}
    
@app.get("/hebrew-number")
def convert_number_get(text: str):
    """
    מקבל טקסט בעברית ומחזיר את המספר העשרוני המתאים.\n
    דוגמה לבקשה:\n
    /hebrew-number?text=אלף מאתיים שלושים וארבע\n
    דוגמה לתגובה:\n
    {
        "number": 1234
    }\n
    דוגמאות נוספות:\n
    - "אלפיים ושבע מאות וחמישים ושמונה"
    - "מיליון וחצי"
    - "2.5 מיליארד"
    """
    try:
        result = hebrew_to_number(text)
        return {"number": result}
    except ValueError as e:
        return {"error": str(e)}