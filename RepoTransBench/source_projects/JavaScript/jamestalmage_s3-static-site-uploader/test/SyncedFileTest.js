const SyncedFile = require('../src/SyncedFile');
const assert = require('assert');

describe('SyncedFile edge/error cases', function() {
  it('should handle impossible state', function() {
    const instance = new SyncedFile({ path: 'foo.txt', hash: '123' }, { path: 'foo.txt', hash: 'abc' });
    instance.local = null; // impossible state for coverage
    instance.remote = null;
    instance.shouldDelete = false;
    instance.shouldUpload = false;
    assert.strictEqual(instance.toString().includes('impossible'), true);
  });

  it('should handle error when hash fails', function(done) {
    // simulate error by passing an invalid file path to hashFile
    instance = new SyncedFile({ path: '/no/this/file.txt', hash: 'x' }, null);
    instance.hashFile = () => { return Promise.reject(new Error('bad hash')); };
    instance.upload().catch(e => {
      assert.strictEqual(e.message, 'bad hash');
      done();
    });
  });

  it('should handle missing local, but present remote (deletion)', function() {
    const instance = new SyncedFile(null, { path: 'foobar', hash: 'yyy' });
    instance.shouldDelete = true;
    assert.strictEqual(instance.action(), 'delete');
  });
});