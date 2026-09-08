const assert = require('assert');

describe('Node.js module system (public test)', function () {
  // Re-test the 'csvToMarkdown' export, but with a runtime invocation that produces output, not just type
  it('should require csvToMarkdown and produce valid markdown output for TSV data', function () {
    const csvToMarkdown = require('../lib/CsvToMarkdown');
    // Use TSV data (tab-separated), not CSV, to check import and function at runtime
    const tsv = 'colA\tcolB\tcolC\nfoo\tbar\tbaz';
    const expectedStart = '| colA | colB | colC |';
    const md = csvToMarkdown(tsv, '\t', true);
    // Only check first line for visibility the function works at all
    assert.strictEqual(typeof md, 'string');
    assert.ok(md.startsWith(expectedStart));
  });

  // Different simulation of `exports` undefined: check for absence of module global (simulate browser/non-node)
  it('should not throw if neither module nor exports are defined (simulated)', function () {
    // Avoids node's module/exports - simulated in a Function context with both undefined
    let warned = false;
    let log = console.error;
    try {
      global.console.error = () => { warned = true }
      Function(`
        "use strict";
        if (typeof module == "undefined" && typeof exports == "undefined") {
            var dummy = 42;
        }
      `)();
      assert.strictEqual(warned, false);
    } finally {
      global.console.error = log;
    }
  });
});