'use strict';

const assert = require('assert');
const path = require('path');
const fs = require('fs');
const findup = require('../index.js');

// This public test suite uses different input/output data than the original tests.
// It covers the same functionality and logic, but operates on different files/patterns/fixtures.
describe('findup-sync (public tests)', function () {
  const fixturesDir = path.join(__dirname, '..', 'test', 'fixtures');
  const altNestedDir = path.join(fixturesDir, 'a', 'b', 'c', 'd', 'e', 'f', 'g');
  const fileToFind = 'g.txt'; // Different file in a different deep dir
  const globPattern = '*.md'; // Use .md instead of .txt for glob pattern

  it('should throw TypeError if patterns is not string or array', function () {
    assert.throws(() => {
      findup(false);
    }, /findup-sync expects a string or array as the first argument/);
    assert.throws(() => {
      findup(undefined);
    }, /findup-sync expects a string or array as the first argument/);
    assert.throws(() => {
      findup(null);
    }, /findup-sync expects a string or array as the first argument/);
  });

  it('should return the correct file when searching by string filename (different file)', function () {
    const cwd = altNestedDir;
    const result = findup(fileToFind, {cwd});
    assert.ok(result, 'Result is falsy');
    assert.strictEqual(path.basename(result), fileToFind);
    assert.ok(fs.existsSync(result));
  });

  it('should return null when file does not exist (other file)', function () {
    const cwd = altNestedDir;
    const result = findup('definitely-not-found-abc.md', {cwd});
    assert.strictEqual(result, null);
  });

  it('should match glob pattern (any md file)', function () {
    const cwd = path.join(fixturesDir, 'a', 'b');
    const result = findup(globPattern, {cwd});
    // Should find a .md file (the only one available is a.md)
    assert.ok(result.endsWith('.md'), 'Should find a .md file');
    assert.ok(fs.existsSync(result));
    assert.strictEqual(path.basename(result), 'a.md');
  });

  it('should match one of the patterns in array (new choices)', function () {
    const cwd = path.join(fixturesDir, 'a', 'b', 'c');
    const files = ['no-such-file.nop', 'ONE.txt'];
    const result = findup(files, {cwd});
    assert.ok(result, 'No match found');
    assert.strictEqual(path.basename(result), 'ONE.txt');
    assert.ok(fs.existsSync(result));
  });

  it('should support absolute cwd (alternative dir)', function () {
    const cwd = path.resolve(path.join(fixturesDir, 'a', 'b', 'c', 'd', 'e'));
    const result = findup('e.txt', {cwd});
    assert.ok(result);
    assert.strictEqual(path.basename(result), 'e.txt');
  });

  it('should support empty patterns array (different directory)', function () {
    const cwd = path.join(fixturesDir, 'a', 'b');
    const result = findup([], {cwd});
    assert.strictEqual(result, null);
  });

  it('should ignore fs.readdirSync errors and return [] (simulate error in different dir)', function () {
    const cwd = path.join(fixturesDir, 'a', 'b');
    const orig = fs.readdirSync;
    fs.readdirSync = () => { throw new Error('Simulated readdir error'); }
    const res = findup(['*.md'], {cwd});
    assert.strictEqual(res, null);
    fs.readdirSync = orig;
  });

  it('should not infinite loop at the filesystem root (search different extension)', function () {
    const root = path.parse(process.cwd()).root;
    const result = findup('not-exist-root-file.zzz', {cwd: root});
    assert.strictEqual(result, null);
  });
});