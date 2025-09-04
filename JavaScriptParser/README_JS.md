# Hebrew Number Parser (JS)

מימוש ב‑JavaScript של מפענח המספרים בעברית.

הבדיקות משתמשות בקובץ `test_cases.json` (כולל VALID ו‑INVALID).

## שימוש
```js
const { hebrewToNumber } = require('./parser');
console.log(hebrewToNumber('מיליון וחצי')); // 1500000
```

## בדיקות
```bash
npm i
npm test
```
