// Extra tests for src/SyncedFile.js
const { expect } = require('chai');
const Q = require('q');
const proxyquire = require('proxyquire');

describe('SyncedFile', function() {
  let SyncedFile, hashVal = 'H', errorSpy;

  beforeEach(() => {
    errorSpy = [];
    const fileUtils = {
      getContentHash: (path) => {
        if (path === 'err.txt') return Q.reject('bad hash');
        return Q.resolve(hashVal);
      }
    };
    SyncedFile = proxyquire('../src/SyncedFile', {
      './file-utils': fileUtils,
      'q': Q
    }).TestHook(fileUtils, Q);
  });

  it('single path: upload when hashes not matching', async() => {
    hashVal = 'x';
    const sf = new SyncedFile('f.txt');
    // File local found, remote found with different hash
    sf.foundFile();
    sf.foundRemote('y');
    const u = await sf.upload;
    expect(u.upload).to.equal(true);
    expect(u.path).to.equal('f.txt');
    const act = await sf.action;
    expect(act.action).to.equal('upload');
  });

  it('single path: nothing to do (hash matches)', async() => {
    hashVal = 'same';
    const sf = new SyncedFile('h.txt');
    sf.foundFile();
    sf.foundRemote('same');
    const act = await sf.action;
    expect(act.action).to.equal('nothing');
    const u = await sf.upload;
    expect(u.upload).to.equal(false);
  });

  it('should handle error in hash', async() => {
    const sf = new SyncedFile('err.txt');
    sf.foundFile();
    sf.foundRemote('abc');
    try {
      await sf.action;
      throw new Error('Should not resolve');
    } catch(e) {
      expect(e).to.equal('bad hash');
    }
  });

  it('should handle file local found, but remote not present', async() => {
    const sf = new SyncedFile('localonly.txt');
    sf.foundFile();
    sf.remoteDone();
    const act = await sf.action;
    expect(act.action).to.equal('upload');
  });

  it('should handle file not local but remote present (delete)', async() => {
    const sf = new SyncedFile('remotefile.txt');
    sf.globDone();
    sf.foundRemote('hhh');
    const act = await sf.action;
    expect(act.action).to.equal('delete');
    const u = await sf.upload;
    expect(u.upload).to.equal(false);
  });

  it('should handle invalid impossible state', async() => {
    // create object, but neither globDone/foundFile nor foundRemote/remoteDone
    const origConsole = console.log;
    let logged = false;
    console.log = () => { logged = true; };
    try {
      const SyncedFileNoHash = proxyquire('../src/SyncedFile', {
        './file-utils': { getContentHash: () => Q.resolve('h') },
        'q': Q
      }).TestHook({ getContentHash: () => Q.resolve('h')}, Q);
      const sf = new SyncedFileNoHash('i.txt');
      // purposely do not call foundFile or globDone or foundRemote or remoteDone
      // expect a rejection thrown on Q.spread
      await Q.delay(10); // allow promises to run
    } catch (e) {
      expect(logged).to.equal(true);
    }
    console.log = origConsole;
  });
});