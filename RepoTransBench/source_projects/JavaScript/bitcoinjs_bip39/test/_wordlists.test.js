// Do not run these tests if source is not present.
const fs = require('fs');
const path = require('path');
const assert = require('assert');

describe('_wordlists', function () {
  const srcPath = path.resolve(__dirname, '../ts_src/_wordlists.ts');
  const wordlistsPath = path.resolve(__dirname, '../ts_src/wordlists/english.json');
  it('should have TypeScript sources for _wordlists', function () {
    assert.ok(fs.existsSync(srcPath), "_wordlists.ts file is missing");
  });
  it('should have at least one wordlist json', function () {
    assert.ok(fs.existsSync(wordlistsPath));
    const arr = require(wordlistsPath);
    assert.ok(Array.isArray(arr));
    assert.strictEqual(arr.length, 2048);
  });
});