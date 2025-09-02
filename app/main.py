from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.parser import hebrew_to_number

app = FastAPI(
    title="Hebrew Number Parser API",
    description="API to convert Hebrew text numbers to decimal numbers",
    version="1.1.0"
)

class NumberRequest(BaseModel):
    text: str

def convert_text_to_number(text: str):
    try:
        number = hebrew_to_number(text)
        return {"number": number}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    examples = [
        "אלף מאתיים שלושים וארבע",
        "מיליון וחצי",
        "2.5 מיליארד",
        "67 אלף",
        "שלוש מאות אלף שש מאות ושבעים",
        "עשרים ושלושה אלף ארבע מאות חמישים ושש"
    ]
    example_cards = "".join([
        f"""
        <div class="example-card">
            <span class="example-text">{ex}</span>
            <span class="copy-icon" onclick="copyToClipboard('{ex}')">&#128203;</span>
        </div>
        """
        for ex in examples
    ])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="he">
    <head>
        <meta charset="UTF-8">
        <title>Hebrew Number Parser</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f9f9f9;
                color: #333;
                direction: rtl;
            }}
            h1 {{ color: #4a90e2; }}
            .container {{
                max-width: 900px;
                margin: auto;
                background: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            #hebrewText {{
                width: 80%;
                padding: 15px;
                font-size: 1.2rem;
                border-radius: 10px;
                border: 1px solid #ccc;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
                margin-bottom: 15px;
            }}
            button {{
                padding: 10px 20px;
                font-size: 1rem;
                background: #4a90e2;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}
            button:hover {{ background: #357ab8; }}
            #result {{
                background: #f0f0f0;
                padding: 20px;
                border-radius: 10px;
                text-align: left;
                font-size: 1.1rem;
                white-space: pre-wrap;
                word-break: break-word;
                margin-top: 15px;
            }}
            h2 {{ margin-top: 40px; }}
            .example-card {{
                background: #e8e8e8;
                padding: 10px 15px;
                margin-bottom: 10px;
                margin-left: 10px;
                margin-right: 10px;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1rem;
            }}
            .example-text {{ flex-grow: 1; }}
            .copy-icon {{
                cursor: pointer;
                margin-left: 10px;
                font-size: 1.2rem;
                color: #4a90e2;
            }}
            .links a {{
                margin-right: 15px;
                color: #4a90e2;
                text-decoration: none;
            }}
            .links a:hover {{ text-decoration: underline; }}
            #result {{
                background: #f0f0f0;
                padding: 20px;
                border-radius: 10px;
                text-align: left; /* חשוב לשמור על מספרים מיושרים לשמאל */
                font-size: 1.1rem;
                white-space: pre-wrap;
                word-break: break-word;
                border: 1px solid #ccc;
                min-height: 35px;
            }}
            .example-card {{
                background: #e8e8e8;
                padding: 10px 15px;
                margin-bottom: 10px;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1rem;
                width: 40%;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hebrew Number Parser API</h1>
            <p>הקלד מספר בעברית ולחץ על "המר" כדי לראות את המספר העשרוני:</p>
            <input type="text" id="hebrewText" placeholder="לדוגמא: אלף מאתיים שלושים וארבע">
            <button onclick="convertNumber()">המר</button>

            <h3>פלט:</h3>
            <pre id="result">---</pre>

            <h2>דוגמאות להרצה</h2>
            {example_cards}

            <div class="links" style="margin-top:40px;">
                <a href="/docs" target="_blank">Swagger UI</a>
                <a href="/redoc" target="_blank">ReDoc</a>
            </div>
        </div>

        <script>
            async function convertNumber() {{
                const text = document.getElementById("hebrewText").value;
                const resultEl = document.getElementById("result");
                try {{
                    const response = await fetch('/hebrew-number', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ text }})
                    }});
                    const data = await response.json();
                    // הפלט נראה יפה עם JSON string יפה
                    resultEl.textContent = data.number.toLocaleString('en-US') || data.error;
                }} catch (err) {{
                    resultEl.textContent = 'Error: ' + err;
                }}
            }}

            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text);
            }}

        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/hebrew-number")
def convert_number_post(req: NumberRequest):
    return convert_text_to_number(req.text)

@app.get("/hebrew-number")
def convert_number_get(text: str):
    return convert_text_to_number(text)
