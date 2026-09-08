const assert = require('assert');
const path = require('path');
const vm = require('vm');

describe('Gruntfile.js (public)', () => {
  it('should not throw when loaded in a VM', () => {
    const fs = require('fs');
    const gruntfilePath = path.resolve(__dirname, '../../Gruntfile.js');
    const gruntSrc = fs.readFileSync(gruntfilePath, 'utf8');
    assert.doesNotThrow(() => {
      vm.runInNewContext(gruntSrc, { module: {}, require: require });
    });
  });
});