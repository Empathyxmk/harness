// Public extra tests for src/SyncedFileCollection.js (different data)
const { expect } = require('chai');
const Q = require('q');
const proxyquire = require('proxyquire');

describe('SyncedFileCollection (public data)', function() {
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

  it('should track foundFile, foundRemote, and resolve allDone (public data)', async () => {
    const coll = new SyncedFileCollection();
    coll.foundFile('baz.pdf');
    coll.foundRemote('quux.doc', 'h456');
    expect(called['baz.pdf.foundFile']).to.be.true;
    expect(called['quux.doc.foundRemote']).to.be.true;
    coll.globDone();
    coll.remoteDone();
    const actions = await coll.allDone;
    expect(actions).to.be.an('array');
    expect(called['baz.pdf.globDone']).to.be.true;
    expect(called['quux.doc.globDone']).to.be.true;
    expect(called['baz.pdf.remoteDone']).to.be.true;
    expect(called['quux.doc.remoteDone']).to.be.true;
  });

  it('should throw if globDone or remoteDone called twice (public data)', () => {
    const coll = new SyncedFileCollection();
    coll.globDone();
    expect(() => coll.globDone()).to.throw();
    const c2 = new SyncedFileCollection();
    c2.remoteDone();
    expect(() => c2.remoteDone()).to.throw();
  });

  it('should throw if foundFile called after globDone (public)', () => {
    const coll = new SyncedFileCollection();
    coll.globDone();
    expect(() => coll.foundFile('qux.png')).to.throw();
  });

  it('should throw if foundRemote called after remoteDone (public)', () => {
    const coll = new SyncedFileCollection();
    coll.remoteDone();
    expect(() => coll.foundRemote('alpha.jpg', 'h2')).to.throw();
  });

  it('should call .globDone/.remoteDone on new after respective done (public)', () => {
    const coll = new SyncedFileCollection();
    coll.globDone();
    coll.remoteDone();
    // This should trigger SyncedFile and call both .globDone and .remoteDone
    coll.foundFile('beta.csv'); // should not throw
    expect(called['beta.csv.globDone']).to.be.true;
    expect(called['beta.csv.remoteDone']).to.be.true;
  });
});