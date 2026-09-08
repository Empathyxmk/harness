const assert = require('assert');
const path = require('path');
const fs = require('fs');

describe('bip39 api surface', function () {
  it('should have TypeScript entrypoint source for index', function () {
    assert.ok(fs.existsSync(path.resolve(__dirname, '../ts_src/index.ts')));
  });
  it('should have type definitions', function () {
    assert.ok(fs.existsSync(path.resolve(__dirname, '../types/index.d.ts')));
  });
});