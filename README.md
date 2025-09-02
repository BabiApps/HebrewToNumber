# Hebrew Number Parser API

מערכת להמרת מספרים בעברית למספרים עשרוניים באמצעות API ו-UI מודרני.

## תיאור
הפרויקט מספק API ועמוד אינטרנט להמרת טקסטים של מספרים בעברית (למשל "אלף מאתיים שלושים וארבע") לערכים עשרוניים.

### דוגמה לשימוש ב-API
- בקשת POST ל-`/hebrew-number` עם גוף:
  ```json
  {
    "text": "אלף מאתיים שלושים וארבע"
  }
  ```
  תגובה:
  ```json
  {
    "number": 1234
  }
  ```

- בקשת GET ל-`/hebrew-number?text=מיליון וחצי`

### דף הבית
עמוד הבית מאפשר להכניס טקסט בעברית ולקבל את המספר העשרוני, כולל דוגמאות מוכנות להעתקה.

## התקנה והרצה
1. התקן את התלויות:
   ```bash
   pip install -r requirements.txt
   ```
2. הרץ את השרת:
   ```bash
   uvicorn app.main:app --reload
   ```
3. פתח את הדפדפן בכתובת:
   [http://localhost:8000](http://localhost:8000)

## תיעוד API
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## דוגמאות להרצה
- "אלף מאתיים שלושים וארבע"
- "מיליון וחצי"
- "2.5 מיליארד"
- "67 אלף"
- "שלוש מאות אלף שש מאות ושבעים"
- "עשרים ושלושה אלף ארבע מאות חמישים ושש"

## תרומה
תרומות, תיקונים ושיפורים יתקבלו בברכה!

---

Hebrew Number Parser API - Convert Hebrew text numbers to decimal integers.
