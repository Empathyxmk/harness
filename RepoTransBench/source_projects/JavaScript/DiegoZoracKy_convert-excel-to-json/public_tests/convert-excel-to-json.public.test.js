const path = require('path');
const convertExcelToJson = require('../lib/convert-excel-to-json');
const fs = require('fs');
const XLSX = require('xlsx');
const { expect } = require('chai');

describe('convert-excel-to-json (public data suite)', function() {
    const testXlsx = path.resolve(__dirname, '../tests/test-data-2.xlsx');
    const testXlsx2 = path.resolve(__dirname, '../tests/test-data.xlsx');
    
    it('should load module and be a function', () => {
        expect(convertExcelToJson).to.be.a('function');
    });

    it('should throw if no source file is provided', () => {
        expect(() => convertExcelToJson({})).to.throw();
    });

    it('should parse a basic sheet to JSON', () => {
        const result = convertExcelToJson({ sourceFile: testXlsx });
        expect(result).to.be.an('object');
        const wsNames = Object.keys(result);
        expect(wsNames.length).to.be.greaterThan(0);
        expect(result[wsNames[0]][0]).to.be.an('object');
    });

    it('should parse only specified sheet', () => {
        const workbook = XLSX.readFile(testXlsx);
        const sheetName = workbook.SheetNames[workbook.SheetNames.length-1];
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: [sheetName]
        });
        expect(result).to.have.keys([sheetName]);
    });

    it('should return empty for non-existent sheet', () => {
        const result = convertExcelToJson({
            sourceFile: testXlsx,
            sheets: [{ name: 'Sheet_DOES_NOT_EXIST' }]
        });
        expect(result['Sheet_DOES_NOT_EXIST']).to.deep.equal([]);
    });

    it('should respect includeEmptyLines=false (default)', () => {
        const res = convertExcelToJson({ sourceFile: testXlsx });
        const ws = Object.keys(res)[0];
        expect(res[ws].every(row => row != null && row != undefined)).to.be.true;
    });

    it('should include empty rows if includeEmptyLines=true', () => {
        const res = convertExcelToJson({ sourceFile: testXlsx, includeEmptyLines: true });
        const ws = Object.keys(res)[0];
        expect(res[ws]).to.be.an('array');
    });

    it('should work with range option and columnToKey', () => {
        const res = convertExcelToJson({
            sourceFile: testXlsx,
            range: 'B2:C4',
            columnToKey: { B: 'bCol', C: 'cCol' }
        });
        const ws = Object.keys(res)[0];
        res[ws].forEach(row => {
            expect(Object.keys(row)).to.satisfy(keys => keys.every(k => ['bCol', 'cCol'].includes(k)));
        });
    });

    it('should support appendData property', () => {
        const workbook = XLSX.readFile(testXlsx2);
        const sheetName = workbook.SheetNames[workbook.SheetNames.length-1];
        const res = convertExcelToJson({
            sourceFile: testXlsx2,
            sheets: [{ name: sheetName, appendData: { bar: 321 } }]
        });
        expect(res[sheetName][0]).to.have.property('bar', 321);
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
            columnToKey: { '*': 'publiccol' }
        });
        const ws = Object.keys(res)[0];
        expect(res[ws][0]).to.be.an('object');
    });

    it('should throw with invalid JSON string as config', () => {
        expect(() => convertExcelToJson('{not json}')).to.throw();
    });
});