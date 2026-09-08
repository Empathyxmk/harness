const path = require('path');
const convertExcelToJson = require('../lib/convert-excel-to-json');
const fs = require('fs');
const assert = require('assert');

const testXlsx = path.resolve(__dirname, 'test-data.xlsx');

describe('convert-excel-to-json: extra cases & edge branches', function () {
    it('should throw on invalid config JSON (string input)', () => {
        assert.throws(() => convertExcelToJson("{notjson: true,}"), SyntaxError);
    });

    it('should use custom header.rows and skip header rows', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            header: { rows: 2 }
        });
        const ws = Object.keys(result)[0];
        // All rows must not contain the header
        assert.ok(result[ws].every(row => !Object.values(row).includes('id')));
    });

    it('should use header.rowToKeys if given (template keying)', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            header: { rowToKeys: 1 }
        });
        assert.ok(typeof result === 'object');
    });

    it('should return empty array for missing sheet (object as entry)', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: [{ name: 'INVALIDSHEETNAME' }]
        });
        assert.deepStrictEqual(result.INVALIDSHEETNAME, []);
    });

    it('should support "source" as Buffer', () => {
        const buf = fs.readFileSync(testXlsx);
        const result = convertExcelToJson({ source: buf });
        assert.ok(Object.keys(result).length > 0);
    });

    it('should accept columnToKey mapping to blank and skip', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            columnToKey: { A: "" }
        });
        const ws = Object.keys(result)[0];
        // All rows have no 'A' property
        assert.ok(result[ws].every(row => !Object.prototype.hasOwnProperty.call(row, '')));
    });

    it('should skip columns not in columnToKey mapping', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            columnToKey: { X: 'notused' }
        });
        const ws = Object.keys(result)[0];
        // Only 'notused' should exist, or empty row
        assert.ok(result[ws].every(row => Object.keys(row).every(k => k === 'notused')));
    });

    it('should work with sheets as strings and objects mixed', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: ['sheet1', { name: 'sheet2' }]
        });
        assert.ok(result['sheet1']);
        assert.ok(result['sheet2']);
    });

    it('should support sheets.numberOfSheetsToGet option', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: { numberOfSheetsToGet: 1 }
        });
        assert.ok(Object.keys(result).length === 1);
    });

    it('should not throw if range excludes all data', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            range: 'Z1:Z2'
        });
        const ws = Object.keys(result)[0];
        assert.ok(Array.isArray(result[ws]));
    });
});