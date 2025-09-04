from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from app.parser import hebrew_to_number
from app.hebrew_format import number_to_hebrew

app = FastAPI(
    title="Hebrew Number Parser API",
    description="API to convert Hebrew text numbers to decimal numbers",
    version="1.2"
)

# mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

class NumberRequest(BaseModel):
    text: str

def convert_text_to_number(text: str):
    try:
        number = hebrew_to_number(text)
        return {"number": number, "hebrew": number_to_hebrew(number)}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    examples = [
    # Up to 10 helpful, somewhat complex examples for users to try
    "מיליון וחצי",
    "מיליארד שלוש מאות מיליון וחצי",
    "שלוש וחצי מיליון",
    "מיליון שלוש מאות אלף חמש מאות וחצי",
    "שבע מאות שמונים ותשע אלף מאתיים שלושים ואחד",
    "עשרים ושלושה אלף ארבע מאות חמישים ושש",
    "מאה אלף חצי",
    "אלף שלוש וחצי",
    "2.5 מיליארד",
    "תשע מאות תשעים ותשע מיליון תשע מאות תשעים ותשע אלף תשע מאות תשעים ותשע",
    ]

    # render template with examples
    return templates.TemplateResponse('index.html', {"request": request, "examples": examples})

@app.post("/hebrew-number")
def convert_number_post(req: NumberRequest):
    return convert_text_to_number(req.text)

@app.get("/hebrew-number")
def convert_number_get(text: str):
    return convert_text_to_number(text)
