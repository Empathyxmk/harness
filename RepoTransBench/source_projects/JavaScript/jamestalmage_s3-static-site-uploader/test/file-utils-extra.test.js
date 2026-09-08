// Additional comprehensive test for src/file-utils.js
const { expect } = require('chai');
const fs = require('fs');
const path = require('path');
const proxyquire = require('proxyquire');
const mockFS = require('mock-fs');

describe('file-utils.js', function() {
  let fileUtils;
  const sampleTxt = 'abc123 lol';
  const sampleFile = 'testfile.txt';
  const testDir = 'testdir';

  before(() => {
    // Prepare a mock filesystem for testing concurrent/multiple files reading
    mockFS({
      [sampleFile]: sampleTxt,
      [testDir]: {
        'a.txt': 'hello',
        'b.txt': 'world'
      }
    });
    fileUtils = proxyquire('../src/file-utils', { fs: require('fs') });
  });

  after(() => {
    mockFS.restore();
  });

  it('should read a file (throttled)', async function() {
    const buf = await fileUtils.getContents(sampleFile, 'utf8');
    expect(buf).to.equal(sampleTxt);
  });

  it('should read multiple files (getContents array)', async function() {
    const files = [path.join(testDir, 'a.txt'), path.join(testDir, 'b.txt')];
    const bufs = await fileUtils.getContents(files, 'utf8');
    expect(bufs).to.deep.equal(['hello', 'world']);
  });

  it('md5 hashes match for strings', function() {
    expect(fileUtils.md5('abc')).to.be.a('string').with.length(32);
    expect(fileUtils.md5('abc')).to.equal(fileUtils.md5('abc'));
  });

  it('getContentHash returns hash for single file', async function() {
    const hash = await fileUtils.getContentHash(sampleFile);
    const expectHash = fileUtils.md5(sampleTxt);
    expect(hash).to.equal(expectHash);
  });

  it('getContentHash returns hashes for array', async function() {
    const files = [path.join(testDir, 'a.txt'), path.join(testDir, 'b.txt')];
    const hashes = await fileUtils.getContentHash(files);
    expect(hashes).to.be.an('array').with.length(2);
    expect(hashes[0]).to.equal(fileUtils.md5('hello'));
    expect(hashes[1]).to.equal(fileUtils.md5('world'));
  });

  it('exists: should resolve true for files and false for missing', async function() {
    expect(await fileUtils.exists(sampleFile)).to.be.true;
    expect(await fileUtils.exists('nope.txt')).to.be.false;
  });

  it('should set MAX_OPEN and throttle open files', function(done) {
    // Set MAX_OPEN very low to force queuing logic
    fileUtils.MAX_OPEN = 1;
    const files = [
      path.join(testDir, 'a.txt'),
      path.join(testDir, 'b.txt'),
      sampleFile
    ];
    Promise.all(files.map(f => fileUtils.getContents(f, 'utf8'))).then(res => {
      expect(res).to.include('hello');
      expect(res).to.include('world');
      expect(res).to.include(sampleTxt);
      done();
    }).catch(done);
  });

  // Clean up: restore MAX_OPEN default after tests
  after(() => { fileUtils.MAX_OPEN = 200; });

  it('get MAX_OPEN returns correct value', () => {
    expect(fileUtils.MAX_OPEN).to.equal(200);
  });
});