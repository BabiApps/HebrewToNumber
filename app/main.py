from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
import json
from app.parser import hebrew_to_number

app = FastAPI(
    title="Hebrew Number Parser API",
    description="API to convert Hebrew text numbers to decimal numbers",
    version="1.1.0"
)

# mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

class NumberRequest(BaseModel):
    text: str

def convert_text_to_number(text: str):
    try:
        number = hebrew_to_number(text)
        return {"number": number}
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
    example_cards = "".join([
        """
        <div class="example-card">
            <span class="example-text">%s</span>
            <span class="copy-icon">&#128203;</span>
        </div>
        """ % ex
        for ex in examples
    ])

    examples_json = json.dumps(examples, ensure_ascii=False)

    html_template = """
    <!DOCTYPE html>
    <html lang="he">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Hebrew Number Parser</title>
        <link href="https://fonts.googleapis.com/css2?family=Alef:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root { --accent: #2563eb; --muted: #6b7280; --bg: #f7f9fc; }
            body {{
                font-family: 'Alef', Arial, sans-serif;
                margin: 0;
                background: var(--bg);
                color: #0f172a;
                direction: rtl;
                -webkit-font-smoothing:antialiased;
            }}
            .wrap {{max-width:1000px;margin:36px auto;padding:24px}}
            .card {{background:#fff;border-radius:14px;padding:28px;box-shadow:0 8px 24px rgba(2,6,23,0.06)}}
            header{{display:flex;align-items:center;justify-content:space-between;gap:16px}}
            h1{{margin:0;color:var(--accent);font-size:1.6rem}}
            .subtitle{{color:var(--muted);margin-top:6px}}

            .controls{{display:flex;gap:12px;align-items:center;margin-top:18px}}
            #hebrewText{{flex:1;padding:12px 14px;border-radius:10px;border:1px solid #e6edf6;font-size:1.05rem}}
            button.primary{{background:var(--accent);color:#fff;border:none;padding:10px 16px;border-radius:10px;cursor:pointer}}
            button.ghost{{background:transparent;border:1px solid #e6edf6;color:var(--accent);padding:8px 12px;border-radius:10px;cursor:pointer}}

            .result{{margin-top:18px;display:flex;gap:12px;align-items:flex-start}}
            .result .box{{flex:1;background:#f8fafc;border-radius:10px;padding:16px;border:1px solid #e6edf6;min-height:56px}}
            .result .value{{font-weight:700;font-size:1.2rem;text-align:left}}
            .small{{color:var(--muted);font-size:0.9rem}}

            .examples-grid{{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}}
            .example-card{{background:linear-gradient(180deg,#fbfdff,#f3f8ff);padding:10px 12px;border-radius:10px;cursor:pointer;border:1px solid #e6edf6;flex:1 1 calc(50% - 12px);min-width:220px;display:flex;align-items:center;justify-content:space-between}}
            .example-card:hover{{box-shadow:0 6px 18px rgba(37,99,235,0.12)}}
            .example-left{{display:flex;flex-direction:column;align-items:flex-end}}
            .example-text{{font-size:0.98rem}}
            .example-note{{font-size:0.8rem;color:var(--muted);margin-top:6px;text-align:left}}

            footer{{margin-top:22px;display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:0.9rem}}

            @media (max-width:640px){{.example-card{{flex:1 1 100%}}header{{flex-direction:column;align-items:flex-start}}}}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="card">
                <header>
                    <div>
                        <h1>Hebrew Number Parser</h1>
                        <div class="subtitle">המרת טקסט מספרי בעברית למספר עשרוני — תומך בחצאים, נקודות, ומכפילים גדולים</div>
                    </div>
                    <div class="small">גרסה 1.1.0 • <a href="/docs" target="_blank">API</a></div>
                </header>

                <div class="controls">
                    <input id="hebrewText" placeholder="לדוגמא: מיליון וחצי" aria-label="Hebrew number input">
                    <button class="primary" onclick="convertNumber()">המר</button>
                    <button class="ghost" onclick="fillExample()">דוגמה אקראית</button>
                </div>

                <div class="result">
                    <div class="box">
                        <div class="small">פלט מפורמט</div>
                        <div id="resultFormatted" class="result-value value">---</div>
                        <div class="small" style="margin-top:6px">JSON: <code id="resultRaw">---</code></div>
                    </div>
                    <div style="width:120px;display:flex;flex-direction:column;gap:8px;">
                        <button class="ghost" onclick="copyResult()">העתק פלט</button>
                        <button class="ghost" onclick="clearAll()">נקה</button>
                    </div>
                </div>

                <h2 style="margin-top:22px">דוגמאות מסובכות — נסו להעתיק ולערוך</h2>
                <div class="examples-grid">
                    __EXAMPLE_CARDS__
                </div>

                <footer>
                    <div>מפתחים: BabiApps</div>
                    <div>הכיווניות: RTL • הממשק פועל ללא חיבור לאינטרנט (חוץ מ־Google Fonts)</div>
                </footer>
            </div>
        </div>

            <script>
            const EXAMPLES = __EXAMPLES_JSON__;
            function formatNumber(n){
                if(n === undefined || n === null) return '---';
                if(typeof n === 'number') return n.toLocaleString('en-US');
                return String(n);
            }

            async function convertNumber(){
                const input = document.getElementById('hebrewText');
                const text = input.value.trim();
                const formatted = document.getElementById('resultFormatted');
                const raw = document.getElementById('resultRaw');
                if(!text){ formatted.textContent = 'הכנס טקסט בעברית'; raw.textContent = '—'; return; }
                formatted.textContent = '…'; raw.textContent = '…';
                try{
                    const res = await fetch('/hebrew-number', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
                    const data = await res.json();
                    if(data.number !== undefined){
                        formatted.textContent = formatNumber(data.number);
                        raw.textContent = JSON.stringify(data, null, 0);
                    } else {
                        formatted.textContent = data.error || 'שגיאה';
                        raw.textContent = JSON.stringify(data, null, 0);
                    }
                }catch(e){ formatted.textContent = 'Error'; raw.textContent = String(e); }
            }

            function copyResult(){
                const raw = document.getElementById('resultRaw').textContent || '';
                navigator.clipboard.writeText(raw);
            }

            function clearAll(){
                document.getElementById('hebrewText').value = '';
                document.getElementById('resultFormatted').textContent = '---';
                document.getElementById('resultRaw').textContent = '---';
            }

            function fillExample(){
                const pick = EXAMPLES[Math.floor(Math.random()*EXAMPLES.length)];
                document.getElementById('hebrewText').value = pick;
            }

            // wire up example cards
            document.addEventListener('DOMContentLoaded', ()=>{
                const container = document.querySelector('.examples-grid');
                // example cards were pre-rendered server-side; attach click handlers
                const cards = container.querySelectorAll('.example-card');
                cards.forEach((card, idx)=>{
                    card.addEventListener('click', ()=>{ document.getElementById('hebrewText').value = EXAMPLES[idx]; });
                });
            });
        </script>
    </body>
    </html>
    """

    # render template with examples
    return templates.TemplateResponse('index.html', {"request": request, "examples": examples})

@app.post("/hebrew-number")
def convert_number_post(req: NumberRequest):
    return convert_text_to_number(req.text)

@app.get("/hebrew-number")
def convert_number_get(text: str):
    return convert_text_to_number(text)
