// Public extra tests for src/SyncedFile.js (different data)
const { expect } = require('chai');
const Q = require('q');
const proxyquire = require('proxyquire');

describe('SyncedFile (public data)', function() {
  let SyncedFile, hashVal = 'HH', errorSpy;

  beforeEach(() => {
    errorSpy = [];
    const fileUtils = {
      getContentHash: (path) => {
        if (path === 'err2.txt') return Q.reject('another bad hash');
        return Q.resolve(hashVal);
      }
    };
    SyncedFile = proxyquire('../src/SyncedFile', {
      './file-utils': fileUtils,
      'q': Q
    }).TestHook(fileUtils, Q);
  });

  it('single path: upload when hashes not matching (public)', async() => {
    hashVal = 'y';
    const sf = new SyncedFile('f2.txt');
    sf.foundFile();
    sf.foundRemote('z');
    const u = await sf.upload;
    expect(u.upload).to.equal(true);
    expect(u.path).to.equal('f2.txt');
    const act = await sf.action;
    expect(act.action).to.equal('upload');
  });

  it('single path: nothing to do (hash matches, public)', async() => {
    hashVal = 'match';
    const sf = new SyncedFile('h2.txt');
    sf.foundFile();
    sf.foundRemote('match');
    const act = await sf.action;
    expect(act.action).to.equal('nothing');
    const u = await sf.upload;
    expect(u.upload).to.equal(false);
  });

  it('should handle error in hash (public)', async() => {
    const sf = new SyncedFile('err2.txt');
    sf.foundFile();
    sf.foundRemote('xyz');
    try {
      await sf.action;
      throw new Error('Should not resolve');
    } catch(e) {
      expect(e).to.equal('another bad hash');
    }
  });

  it('should handle file local found, but remote not present (public)', async() => {
    const sf = new SyncedFile('specialonly.txt');
    sf.foundFile();
    sf.remoteDone();
    const act = await sf.action;
    expect(act.action).to.equal('upload');
  });

  it('should handle file not local but remote present (delete, public)', async() => {
    const sf = new SyncedFile('remotefile2.txt');
    sf.globDone();
    sf.foundRemote('iii');
    const act = await sf.action;
    expect(act.action).to.equal('delete');
    const u = await sf.upload;
    expect(u.upload).to.equal(false);
  });

  it('should handle invalid impossible state (public)', async() => {
    // create object, but neither globDone/foundFile nor foundRemote/remoteDone
    const origConsole = console.log;
    let logged = false;
    console.log = () => { logged = true; };
    try {
      const SyncedFileNoHash = proxyquire('../src/SyncedFile', {
        './file-utils': { getContentHash: () => Q.resolve('hh') },
        'q': Q
      }).TestHook({ getContentHash: () => Q.resolve('hh')}, Q);
      const sf = new SyncedFileNoHash('j.txt');
      await Q.delay(10); // allow promises to run
    } catch (e) {
      expect(logged).to.equal(true);
    }
    console.log = origConsole;
  });
});