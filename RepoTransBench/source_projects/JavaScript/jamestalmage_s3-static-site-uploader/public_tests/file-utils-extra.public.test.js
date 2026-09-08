// Public comprehensive tests for src/file-utils.js (different data and files)
const { expect } = require('chai');
const fs = require('fs');
const path = require('path');
const proxyquire = require('proxyquire');
const mockFS = require('mock-fs');

describe('file-utils.js (public data)', function() {
  let fileUtils;
  const sampleTxt = 'zxc987 yikes';
  const sampleFile = 'publicfile1.txt';
  const testDir = 'public_testdir';

  before(() => {
    // Prepare a mock filesystem with new file/data for public test
    mockFS({
      [sampleFile]: sampleTxt,
      [testDir]: {
        'x.txt': 'foo',
        'y.txt': 'bar'
      }
    });
    fileUtils = proxyquire('../src/file-utils', { fs: require('fs') });
  });

  after(() => {
    mockFS.restore();
  });

  it('should read a file (throttled, public)', async function() {
    const buf = await fileUtils.getContents(sampleFile, 'utf8');
    expect(buf).to.equal(sampleTxt);
  });

  it('should read multiple files (getContents array, public)', async function() {
    const files = [path.join(testDir, 'x.txt'), path.join(testDir, 'y.txt')];
    const bufs = await fileUtils.getContents(files, 'utf8');
    expect(bufs).to.deep.equal(['foo', 'bar']);
  });

  it('md5 hashes match for strings (public)', function() {
    expect(fileUtils.md5('def')).to.be.a('string').with.length(32);
    expect(fileUtils.md5('def')).to.equal(fileUtils.md5('def'));
  });

  it('getContentHash returns hash for single file (public)', async function() {
    const hash = await fileUtils.getContentHash(sampleFile);
    const expectHash = fileUtils.md5(sampleTxt);
    expect(hash).to.equal(expectHash);
  });

  it('getContentHash returns hashes for array (public)', async function() {
    const files = [path.join(testDir, 'x.txt'), path.join(testDir, 'y.txt')];
    const hashes = await fileUtils.getContentHash(files);
    expect(hashes).to.be.an('array').with.length(2);
    expect(hashes[0]).to.equal(fileUtils.md5('foo'));
    expect(hashes[1]).to.equal(fileUtils.md5('bar'));
  });

  it('exists: should resolve true for files and false for missing (public)', async function() {
    expect(await fileUtils.exists(sampleFile)).to.be.true;
    expect(await fileUtils.exists('definitely_missing.pub')).to.be.false;
  });

  it('should set MAX_OPEN and throttle open files (public)', function(done) {
    // Set MAX_OPEN very low to force queuing logic
    fileUtils.MAX_OPEN = 1;
    const files = [
      path.join(testDir, 'x.txt'),
      path.join(testDir, 'y.txt'),
      sampleFile
    ];
    Promise.all(files.map(f => fileUtils.getContents(f, 'utf8'))).then(res => {
      expect(res).to.include('foo');
      expect(res).to.include('bar');
      expect(res).to.include(sampleTxt);
      done();
    }).catch(done);
  });

  // Clean up: restore MAX_OPEN default after tests
  after(() => { fileUtils.MAX_OPEN = 200; });

  it('get MAX_OPEN returns correct value (public)', () => {
    expect(fileUtils.MAX_OPEN).to.equal(200);
  });
});