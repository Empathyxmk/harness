const assert = require('assert');
const SyncedFileCollection = require('../src/SyncedFileCollection');

describe('SyncedFileCollection - edge cases', function() {
  it('should throw when globDone called twice', function() {
    const col = new SyncedFileCollection();
    col.globDone();
    assert.throws(() => col.globDone(), /Glob is supposed to be done/);
  });

  it('should throw when remoteDone called twice', function() {
    const col = new SyncedFileCollection();
    col.remoteDone();
    assert.throws(() => col.remoteDone(), /Remote listing is supposed to be done/);
  });

  it('should throw if foundFile called after globDone', function() {
    const col = new SyncedFileCollection();
    col.globDone();
    assert.throws(() => col.foundFile('foo'), /Glob is supposed to be done/);
  });

  it('should throw if foundRemote called after remoteDone', function() {
    const col = new SyncedFileCollection();
    col.remoteDone();
    assert.throws(() => col.foundRemote('bar'), /Remote listing is supposed to be done/);
  });
});