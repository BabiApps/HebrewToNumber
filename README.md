# Hebrew Number Parser

ממיר ביטויי מספר בעברית לערכים מספריים – (כולל API ו‑UI).

## מה זה עושה
- מפענח יחידות/עשרות/מאות (כולל “שבע מאות”) ומכפילים: **אלף/אלפים/מיליון/מיליארד**.
- תומך בשברים: **חצי**, **רבע** (גם אחרי מכפיל כמו “מיליון וחצי”).
- תומך בעשרוניות עם **“נקודה”**: ספרות (“נקודה אפס אפס חמש”) או ביטוי גדול (“נקודה שבע מאות ושבע”, “נקודה שבע אלף”).
- קשיח: ניסוחים לא תקינים (למשל “חמישים אלפיים”, “אלף שמונים שבעים”, “מיליון מיליון”) זורקים `ValueError`.

## איך משתמשים?
```python
from app.parser import hebrew_to_number

print(hebrew_to_number("אלף מאה וחמישים"))           # 1150
print(hebrew_to_number("מיליון וחצי"))               # 1500000.0
print(hebrew_to_number("חמישים ושש נקודה שבע אלף"))   # 56.7000
print(hebrew_to_number("אלף שלוש ורבע"))             # 1003.25
```

(קיימת גרסה גם ב JavaScript)

## API  (FastAPI)
- GET: `/hebrew-number?text=אלף מאה וחמישים`
- POST: `/hebrew-number` עם JSON: `{ "text": "אלף מאה וחמישים" }`
- GET: `/` - דף נחיתה עם ממשק נחמד

### הרצה מקומית
```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

## בדיקות
```bash
pytest -q
```

---
מצאתם בעיה או רוצים לשפר? מוזמנים לפתוח **Issue** או להגיש **Pull Request**.

Made By BabiApps