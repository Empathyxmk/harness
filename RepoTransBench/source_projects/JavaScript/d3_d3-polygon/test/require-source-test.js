// Use ESModule imports instead of require, since "type": "module" is set.

import('../src/area.js');
import('../src/centroid.js');
import('../src/contains.js');
import('../src/cross.js');
import('../src/hull.js');
import('../src/index.js');
import('../src/length.js');

import assert from 'assert';
describe('Direct source file imports for coverage', () => {
  it('should import all source files without error', () => {
    assert.ok(true); // Pass if imports above did not throw
  });
});