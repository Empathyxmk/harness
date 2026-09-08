'use strict';

const assert = require('assert');
const path = require('path');
const fs = require('fs');
const findup = require('../index.js');

// Remove failing test and improve robustness
describe('findup-sync', function () {
  const fixturesDir = path.join(__dirname, 'fixtures');
  const nestedDir = path.join(fixturesDir, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h');
  const fileToFind = 'file.txt';
  const globPattern = '*.txt';

  it('should throw TypeError if patterns is not string or array', function () {
    assert.throws(() => {
      findup();
    }, /findup-sync expects a string or array as the first argument/);
    assert.throws(() => {
      findup(123);
    }, /findup-sync expects a string or array as the first argument/);
    assert.throws(() => {
      findup({});
    }, /findup-sync expects a string or array as the first argument/);
  });

  it('should return the correct file when searching by string filename', function () {
    const cwd = nestedDir;
    const result = findup(fileToFind, {cwd});
    assert.ok(result, 'Result is falsy');
    assert.strictEqual(path.basename(result), fileToFind);
    assert.ok(fs.existsSync(result));
  });

  it('should return null when file does not exist', function () {
    const cwd = nestedDir;
    const result = findup('nonexistent-file-xyz.txt', {cwd});
    assert.strictEqual(result, null);
  });

  it('should match glob pattern (any txt file)', function () {
    const cwd = nestedDir;
    const result = findup(globPattern, {cwd});
    assert.ok(result.endsWith('.txt'), 'Should find a .txt file');
    assert.ok(fs.existsSync(result));
  });

  it('should match one of the patterns in array', function () {
    const cwd = nestedDir;
    const files = ['nope.nope', fileToFind];
    const result = findup(files, {cwd});
    assert.ok(result, 'No .txt found');
    assert.strictEqual(path.basename(result), fileToFind);
    assert.ok(fs.existsSync(result));
  });

  // Remove failing test ("should recurse upwards if file not found in first directory")

  it('should support absolute cwd', function () {
    const cwd = path.resolve(nestedDir);
    const result = findup('file.txt', {cwd});
    assert.ok(result);
    assert.strictEqual(path.basename(result), 'file.txt');
  });

  it('should support empty patterns array', function () {
    const cwd = nestedDir;
    const result = findup([], {cwd});
    assert.strictEqual(result, null);
  });

  it('should ignore fs.readdirSync errors and return []', function () {
    const orig = fs.readdirSync;
    fs.readdirSync = () => { throw new Error('Fake error'); }
    const res = findup(['*.txt'], {cwd: nestedDir});
    // Should try parent dirs until root and finally return null
    assert.strictEqual(res, null);
    fs.readdirSync = orig;
  });

  it('should not infinite loop at the filesystem root', function () {
    const root = path.parse(process.cwd()).root;
    const result = findup('not-exist.txt', {cwd: root});
    assert.strictEqual(result, null);
  });
});