const assert = require('assert');
const fs = require('fs');
const path = require('path');

describe('util/wordlists.js', function () {
  // There may not be a util/wordlists.js if only TS code is present
  const jsPath = path.resolve(__dirname, '../util/wordlists.js');
  it('should have util/wordlists.js file if built', function () {
    assert.ok(fs.existsSync(jsPath));
  });
  it('should not throw if required (only syntax check)', function () {
    if (fs.existsSync(jsPath)) require(jsPath);
  });
});