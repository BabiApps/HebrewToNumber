import { hebrewToNumber } from './parser';
import fs from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const data = JSON.parse(fs.readFileSync(__dirname + '/test_cases.json', 'utf8'));

describe('Hebrew Number Parser (JS) — parity & invalids', () => {
  test.each(data.valid.map(v => [v.text, v.expected]))('valid: %s', (text, expected) => {
    const val = hebrewToNumber(text);
    expect(val).toBeCloseTo(expected, 9);
  });

  test.each(data.invalid.map(t => [t]))('invalid (should throw): %s', (text) => {
    expect(() => hebrewToNumber(text)).toThrow();
  });
});
