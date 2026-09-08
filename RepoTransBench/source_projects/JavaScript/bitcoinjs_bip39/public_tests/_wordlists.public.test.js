// Check for a different ts_src file and a different wordlist for public verification.
const fs = require('fs');
const path = require('path');
const assert = require('assert');

describe('_wordlists (public)', function () {
  const altSrcPath = path.resolve(__dirname, '../ts_src/_wordlists.ts');
  const altWordlistsPath = path.resolve(__dirname, '../ts_src/wordlists/french.json');
  it('should have TypeScript sources for _wordlists.ts (public)', function () {
    // Still looking for _wordlists.ts, but naming matches file previously used for source check
    assert.ok(fs.existsSync(altSrcPath), "_wordlists.ts file is missing (public)");
  });
  it('should have at least one non-english wordlist json (public)', function () {
    assert.ok(fs.existsSync(altWordlistsPath));
    const arr = require(altWordlistsPath);
    assert.ok(Array.isArray(arr));
    assert.strictEqual(arr.length, 2048);
  });
});