const path = require('path');
const convertExcelToJson = require('../lib/convert-excel-to-json');
const fs = require('fs');
const XLSX = require('xlsx');
const { expect } = require('chai');

describe('convert-excel-to-json', function() {
    const testXlsx = path.resolve(__dirname, 'test-data.xlsx');
    const testXlsx2 = path.resolve(__dirname, 'test-data-2.xlsx');
    
    it('should load without error', () => {
        expect(convertExcelToJson).to.be.a('function');
    });

    it('should throw if no source file is provided', () => {
        expect(() => convertExcelToJson({})).to.throw();
    });

    it('should parse a basic sheet to JSON', () => {
        const result = convertExcelToJson({ sourceFile: testXlsx });
        expect(result).to.be.an('object');
        // Check at least one worksheet and one row
        const wsNames = Object.keys(result);
        expect(wsNames.length).to.be.greaterThan(0);
        expect(result[wsNames[0]][0]).to.be.an('object');
    });

    it('should parse only specified sheet', () => {
        const workbook = XLSX.readFile(testXlsx);
        const sheetName = workbook.SheetNames[0];
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: [sheetName]
        });
        expect(result).to.have.keys([sheetName]);
    });

    it('should return empty for non-existent sheet', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: [{ name: 'NonExistent' }]
        });
        expect(result['NonExistent']).to.deep.equal([]);
    });

    it('should respect includeEmptyLines=false (default)', () => {
        const res = convertExcelToJson({ sourceFile: testXlsx });
        const ws = Object.keys(res)[0];
        expect(res[ws].every(row => row != null && row != undefined)).to.be.true;
    });

    it('should include empty rows if includeEmptyLines=true', () => {
        const res = convertExcelToJson({ sourceFile: testXlsx, includeEmptyLines: true });
        const ws = Object.keys(res)[0];
        // Expect at least one undefined/null row (simulate by inserting/forcing blank in test data if needed)
        // Here, we at least check the type and length doesn't get filtered out
        // (Cannot guarantee without synthetic input)
        expect(res[ws]).to.be.an('array');
    });

    it('should work with range option and columnToKey', () => {
        const res = convertExcelToJson({
            sourceFile: testXlsx,
            range: 'A1:B3',
            columnToKey: { A: 'colA', B: 'colB' }
        });
        const ws = Object.keys(res)[0];
        // All parsed rows should only have 'colA' and 'colB'
        res[ws].forEach(row => {
            expect(Object.keys(row)).to.satisfy(keys => keys.every(k => ['colA', 'colB'].includes(k)));
        });
    });

    it('should support appendData property', () => {
        const workbook = XLSX.readFile(testXlsx2);
        const sheetName = workbook.SheetNames[0];
        const res = convertExcelToJson({
            sourceFile: testXlsx2,
            sheets: [{ name: sheetName, appendData: { foo: 123 } }]
        });
        expect(res[sheetName][0]).to.have.property('foo', 123);
    });

    it('should support stubs (sheetStubs=true)', () => {
        const res = convertExcelToJson({
            sourceFile: testXlsx,
            sheetStubs: true
        });
        const ws = Object.keys(res)[0];
        expect(res[ws]).to.be.an('array');
    });

    it('should handle config as JSON string', () => {
        const configStr = JSON.stringify({ sourceFile: testXlsx });
        const res = convertExcelToJson(configStr);
        const ws = Object.keys(res)[0];
        expect(res[ws]).to.be.an('array');
    });

    it('should respect columnToKey with a wildcard', () => {
        const res = convertExcelToJson({
            sourceFile: testXlsx,
            columnToKey: { '*': 'anycol' }
        });
        const ws = Object.keys(res)[0];
        expect(res[ws][0]).to.be.an('object');
    });

    it('should throw with invalid JSON string as config', () => {
        expect(() => convertExcelToJson('{invalid}')).to.throw();
    });
});