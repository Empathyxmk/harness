const assert = require('assert');
const fs = require('fs');

describe('project build (public test)', function () {
  it('should have tslint.json config for build (public alt config check)', function () {
    assert.ok(fs.existsSync('tslint.json'), 'tslint.json missing');
  });
});