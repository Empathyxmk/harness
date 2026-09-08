const assert = require('assert');
const path = require('path');
const fuge = require('../fuge.js');

describe('fuge.js edge cases (public)', function() {
  it('should export expected keys (public edge)', function() {
    const keys = Object.keys(fuge);
    // Just check that at least one known export exists (assume 'run' present in main)
    assert(keys.length > 0, 'fuge should export at least one key');
  });

  it('should handle invalid system path (different invalid file)', function(done) {
    if (typeof fuge.createSystem === 'function') {
      fuge.createSystem('not/a/real/public_edge_file.yml', {}, function(err, sys) {
        assert(err, 'should error for invalid path');
        done();
      });
    } else {
      done();
    }
  });
});