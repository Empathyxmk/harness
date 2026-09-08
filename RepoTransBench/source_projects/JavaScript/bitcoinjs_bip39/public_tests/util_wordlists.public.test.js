const assert = require('assert');
const fs = require('fs');
const path = require('path');

describe('util/wordlists.js (public)', function () {
  // Intentionally use a different approach to access the util/wordlists.js path for public test
  const jsPath = path.join(__dirname, '..', 'util', 'wordlists.js');
  it('should exist as a file on disk (public alt check)', function () {
    // Use statSync and isFile for a different code path
    let exists = false;
    try {
      exists = fs.statSync(jsPath).isFile();
    } catch (e) {}
    assert.ok(exists, 'util/wordlists.js file does not exist');
  });
  it('should be requireable and have no exception (public)', function () {
    if (fs.existsSync(jsPath)) {
      let threw = false;
      try {
        require(jsPath);
      } catch (e) {
        threw = true;
      }
      assert.strictEqual(threw, false, "util/wordlists.js should not throw when required");
    }
  });
});