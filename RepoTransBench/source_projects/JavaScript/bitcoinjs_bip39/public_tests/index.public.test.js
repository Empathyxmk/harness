const assert = require('assert');
const path = require('path');
const fs = require('fs');

describe('bip39 api surface (public)', function () {
  it('should have TypeScript wordlists source for index (public)', function () {
    assert.ok(fs.existsSync(path.resolve(__dirname, '../ts_src/wordlists/italian.json')));
  });
  it('should have wordlists type definitions (public)', function () {
    assert.ok(fs.existsSync(path.resolve(__dirname, '../types/wordlists.d.ts')));
  });
});