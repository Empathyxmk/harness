'use strict';

const excelToJson = require('../');
const assert = require('assert');
const child_process = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

const publicSourceFile = path.join(__dirname, '../tests/test-data-2.xlsx');
const publicSourceBuffer = fs.readFileSync(publicSourceFile);

describe('Public Conversion Tests', function() {
  it('should throw an error if config missing sourceFile/source', function() {
    assert.throws(() => excelToJson({ sheets: []}), Error);
  });

	describe('Simple :: Object Literal with test-data-2.xlsx', function() {
		basicPublic({
			sourceFile: publicSourceFile
		});
	});

	describe('Simple :: JSON String as param', function() {
		basicPublic(JSON.stringify({
			sourceFile: publicSourceFile
		}));
	});

	describe('Simple :: Buffer as source', function() {
		basicPublic({
			source: publicSourceBuffer
		});
	});

	describe('"sheets" config public', function() {

		describe('get "Data" and "Summary" with mixed type list', function() {
			const jsonResult = excelToJson({
				sourceFile: publicSourceFile,
				sheets: ['Data', { name: 'Summary' }]
			});

			it('should be an Object', function() {
				assert.equal(jsonResult.constructor, Object);
			});

			it('should have two result sets', function() {
				assert.equal(Object.keys(jsonResult).length, 2);
			});

			describe('Data sheet', function() {

				it('should have a key named "Data"', function() {
					assert.notEqual(jsonResult.Data, undefined);
				});

				describe('result data', function() {

					it('should have at least 3 "rows"', function() {
						assert.ok(jsonResult.Data.length >= 3);
					});

					it('should have at least the columns "A" and "B"', function() {
						const keys = Object.keys(jsonResult.Data[0]);
						assert.ok(keys.includes('A') && keys.includes('B'));
					});

					it('should have the header values on the first row', function() {
						const firstRow = jsonResult.Data[0];
						assert.ok(firstRow.A && typeof firstRow.A === 'string');
					});
				});
			});

			describe('Summary sheet', function() {

				it('should have a key named "Summary"', function() {
					assert.notEqual(jsonResult.Summary, undefined);
				});

				describe('result data', function() {
					it('should have at least 1 "row"', function() {
						assert.ok(jsonResult.Summary.length >= 1);
					});

					it('should have the column "A"', function() {
						assert.ok(Object.keys(jsonResult.Summary[0]).includes('A'));
					});
				});
			});
		});

		describe('get only "Summary" sheet', function() {

			const jsonResult = excelToJson({
				sourceFile: publicSourceFile,
				sheets: ['Summary']
			});

			it('should be an Object', function() {
				assert.equal(jsonResult.constructor, Object);
			});

			it('should have one result set', function() {
				assert.equal(Object.keys(jsonResult).length, 1);
			});

			describe('Data', function() {
				it('should not have a key named "Data"', function() {
					assert.equal(jsonResult.Data, undefined);
				});
			});

			describe('Summary', function() {
				it('should have a key named "Summary"', function() {
					assert.notEqual(jsonResult.Summary, undefined);
				});

				describe('result data', function() {
					it('should have at least one "row"', function() {
						assert.ok(jsonResult.Summary.length >= 1);
					});

					it('should have column "A"', function() {
						assert.ok(Object.keys(jsonResult.Summary[0]).includes('A'));
					});
				});
			});
		});
	});
});


function basicPublic(param) {
	describe('Public basic invocation', function() {
		let result;
		it('should convert and return Object', function() {
			result = excelToJson(param);
			assert.equal(typeof result, 'object');
		});
		it('should have at least 1 worksheet', function() {
			assert.ok(Object.keys(result).length >= 1);
		});
		it('should have some rows of data', function() {
			const ws = Object.keys(result)[0];
			assert.ok(Array.isArray(result[ws]));
			assert.ok(result[ws].length > 0);
		});
	});
}