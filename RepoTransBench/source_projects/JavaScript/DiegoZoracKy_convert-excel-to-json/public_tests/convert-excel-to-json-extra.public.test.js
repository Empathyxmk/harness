const path = require('path');
const convertExcelToJson = require('../lib/convert-excel-to-json');
const fs = require('fs');
const assert = require('assert');

const testXlsx = path.resolve(__dirname, '../tests/test-data-2.xlsx');

describe('convert-excel-to-json: public extra cases & edge branches', function () {
    it('should throw on invalid config JSON (string input)', () => {
        assert.throws(() => convertExcelToJson("{foo: true notvalid}"), SyntaxError);
    });

    it('should use custom header.rows and skip header rows', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            header: { rows: 1 }
        });
        const ws = Object.keys(result)[0];
        // All rows must not contain the first header string present in test-data-2.xlsx
        assert.ok(result[ws].every(row => !Object.values(row).includes('Name')));
    });

    it('should use header.rowToKeys if given (template keying)', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            header: { rowToKeys: 2 }
        });
        assert.ok(typeof result === 'object');
    });

    it('should return empty array for missing sheet (object as entry)', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: [{ name: 'NO_SHEET' }]
        });
        assert.deepStrictEqual(result.NO_SHEET, []);
    });

    it('should support "source" as Buffer', () => {
        const buf = fs.readFileSync(testXlsx);
        const result = convertExcelToJson({ source: buf });
        assert.ok(Object.keys(result).length > 0);
    });

    it('should accept columnToKey mapping to blank and skip', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            columnToKey: { B: "" }
        });
        const ws = Object.keys(result)[0];
        assert.ok(result[ws].every(row => !Object.prototype.hasOwnProperty.call(row, '')));
    });

    it('should skip columns not in columnToKey mapping', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            columnToKey: { Y: 'notpresent' }
        });
        const ws = Object.keys(result)[0];
        assert.ok(result[ws].every(row => Object.keys(row).every(k => k === 'notpresent')));
    });

    it('should work with sheets as strings and objects mixed', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: ['Data', { name: 'Summary' }]
        });
        assert.ok(result['Data'] || result['Summary']);
    });

    it('should support sheets.numberOfSheetsToGet option', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: { numberOfSheetsToGet: 2 }
        });
        assert.ok(Object.keys(result).length === 2 || Object.keys(result).length === 1);
    });

    it('should not throw if range excludes all data', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            range: 'Q10:Q20'
        });
        const ws = Object.keys(result)[0];
        assert.ok(Array.isArray(result[ws]));
    });
});