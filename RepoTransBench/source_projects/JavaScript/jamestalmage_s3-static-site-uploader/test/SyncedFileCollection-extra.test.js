// Extra tests for src/SyncedFileCollection.js
const { expect } = require('chai');
const Q = require('q');
const proxyquire = require('proxyquire');

describe('SyncedFileCollection', function() {
  let SyncedFileCollection, SyncedFileMock, called = {};

  beforeEach(() => {
    called = {};
    SyncedFileMock = function(path) {
      this.path = path;
      this.globbed = false;
      this.remoted = false;
      this.action = Q.resolve({ action: 'ok', path });
      this.globDone = function() { called[path+'.globDone'] = true; this.globbed = true; };
      this.remoteDone = function() { called[path+'.remoteDone'] = true; this.remoted = true; };
      this.foundFile = function() { called[path+'.foundFile'] = true; this.ff =true; };
      this.foundRemote = function() { called[path+'.foundRemote'] = true; this.fr =true; };
    };
    SyncedFileCollection = proxyquire('../src/SyncedFileCollection', {
      './SyncedFile': SyncedFileMock,
      'q': Q
    }).TestHook(SyncedFileMock, Q);
  });

  it('should track foundFile, foundRemote, and resolve allDone', async () => {
    const coll = new SyncedFileCollection();
    coll.foundFile('foo.txt');
    coll.foundRemote('bar.txt', 'h123');
    expect(called['foo.txt.foundFile']).to.be.true;
    expect(called['bar.txt.foundRemote']).to.be.true;
    coll.globDone();
    coll.remoteDone();
    const actions = await coll.allDone;
    expect(actions).to.be.an('array');
    expect(called['foo.txt.globDone']).to.be.true;
    expect(called['bar.txt.globDone']).to.be.true;
    expect(called['foo.txt.remoteDone']).to.be.true;
    expect(called['bar.txt.remoteDone']).to.be.true;
  });

  it('should throw if globDone or remoteDone called twice', () => {
    const coll = new SyncedFileCollection();
    coll.globDone();
    expect(() => coll.globDone()).to.throw();
    const c2 = new SyncedFileCollection();
    c2.remoteDone();
    expect(() => c2.remoteDone()).to.throw();
  });

  it('should throw if foundFile called after globDone', () => {
    const coll = new SyncedFileCollection();
    coll.globDone();
    expect(() => coll.foundFile('foo.txt')).to.throw();
  });

  it('should throw if foundRemote called after remoteDone', () => {
    const coll = new SyncedFileCollection();
    coll.remoteDone();
    expect(() => coll.foundRemote('foo.txt', 'h')).to.throw();
  });

  it('should call .globDone/.remoteDone on new after respective done', () => {
    const coll = new SyncedFileCollection();
    coll.globDone();
    coll.remoteDone();
    // This should trigger SyncedFile and call both .globDone and .remoteDone
    coll.foundFile('later.txt'); // should not throw
    expect(called['later.txt.globDone']).to.be.true;
    expect(called['later.txt.remoteDone']).to.be.true;
  });
});