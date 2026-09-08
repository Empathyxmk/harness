const assert = require('assert');
const fs = require('fs');

describe('project build', function () {
  it('should have tsconfig.json file for build', function () {
    assert.ok(fs.existsSync('tsconfig.json'), 'tsconfig.json missing');
  });
});