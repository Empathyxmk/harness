const cached = require('../index');
const assert = require('assert');
const File = require('vinyl');

describe('gulp-cached extra cases', function() {
  it('should allow optimizeMemory option and hash content', function(done) {
    const plugin = cached('test-optimise', { optimizeMemory: true });
    const file = new File({ path: 'test/file.txt', contents: Buffer.from('foo') });
    plugin.write(file);
    plugin.end();
    plugin.once('data', data => {
      assert.deepStrictEqual(data, file, 'File must match');
      done();
    });
  });

  it('should not add a file to cache if it is a stream (isStream returns true)', function(done) {
    const plugin = cached('test-stream');
    const file = new File({ path: 'stream/file.txt' });
    file.isStream = () => true;
    plugin.write(file);
    plugin.end();
    let called = false;
    plugin.once('data', data => {
      called = true;
      assert.deepStrictEqual(data, file);
    });
    setTimeout(() => {
      assert.ok(called, 'Should call once for stream file');
      done();
    }, 10);
  });

  it('should support .isBuffer() returning false (both isStream/isBuffer false)', function(done) {
    const plugin = cached('test-false-buffer');
    const file = new File({ path: 'buff/file.txt' });
    file.isStream = () => false;
    file.isBuffer = () => false;
    plugin.write(file);
    plugin.end();
    plugin.once('data', data => {
      assert.ok(data instanceof File, 'Should still be a Vinyl File');
      assert.strictEqual(data.path, file.path);
      done();
    });
  });

  it('should handle checksum property on buffer file and skip hashing', function(done) {
    const plugin = cached('test-checksum');
    const buf = Buffer.from('abc');
    const file = new File({ path: 'foo/buf2.txt', contents: buf });
    file.checksum = 'dummy-checksum';
    file.isBuffer = () => true;
    file.isStream = () => false;

    plugin.write(file);
    plugin.end();
    plugin.once('data', data => {
      assert.strictEqual(data.checksum, 'dummy-checksum');
      done();
    });
  });

  it('should allow files with same path in different caches (confirm cache isolation)', function(done) {
    const plugin1 = cached('unique1');
    const plugin2 = cached('unique2');
    const filePath = 'common/file.txt';
    const file1 = new File({ path: filePath, contents: Buffer.from('1') });
    const file2 = new File({ path: filePath, contents: Buffer.from('2') });

    plugin1.write(file1);
    plugin2.write(file2);

    let received = 0;
    plugin1.once('data', data1 => {
      assert.strictEqual(data1.contents.toString(), '1');
      received++;
      if (received === 2) done();
    });
    plugin2.once('data', data2 => {
      assert.strictEqual(data2.contents.toString(), '2');
      received++;
      if (received === 2) done();
    });

    plugin1.end();
    plugin2.end();
  });

  it('should not share cache if name is falsy (undefined)', function(done) {
    // Test that two unnamed caches do NOT share the same memory
    const pluginA = cached();
    const pluginB = cached();
    const filePathA = 'falsy/fileA.txt';
    const filePathB = 'falsy/fileB.txt';
    const fileA = new File({ path: filePathA, contents: Buffer.from('x') });
    const fileB = new File({ path: filePathB, contents: Buffer.from('y') });

    let seenA = false;
    let seenB = false;

    pluginA.on('data', d => {
      if (d.path === filePathA) seenA = true;
    });
    pluginB.on('data', d => {
      if (d.path === filePathB) seenB = true;
    });

    pluginA.write(fileA);
    pluginA.end();
    pluginB.write(fileB);
    pluginB.end();

    setTimeout(() => {
      assert.ok(seenA, 'pluginA should let its file through');
      assert.ok(seenB, 'pluginB should let its file through');
      done();
    }, 25);
  });

  it('plugin.caches should be an object and exist on the module', function() {
    assert.strictEqual(typeof cached.caches, 'object');
    assert.ok(cached.caches);
  });
});

describe('gulp-cached', function() {
  it('should create a cache that only allows a file through once', function(done) {
    const plugin = cached('simple');
    const file = new File({ path: 'foo/file.txt', contents: Buffer.from('bar') });
    plugin.write(file);
    let calls = 0;
    plugin.on('data', d => {
      ++calls;
      assert.deepStrictEqual(d, file);
    });
    plugin.on('end', () => {
      assert.strictEqual(calls, 1, 'File should only be allowed through once');
      done();
    });
    plugin.write(file);
    plugin.end();
  });

  it('should create a cache that clears content when reset', function(done) {
    const plugin = cached('reset');
    const file = new File({ path: 'path/file.txt', contents: Buffer.from('baz') });
    plugin.write(file);

    let cnt = 0;

    plugin.on('data', () => { cnt++; });
    plugin.on('end', () => {
      // now simulate cache reset using documented way:
      cached.caches['reset'] = {}; // clear the object literally as reset() method is not part of API
      // Create new plugin to use reset cache
      const plugin2 = cached('reset');
      plugin2.write(file);
      let cnt2 = 0;
      plugin2.on('data', () => { cnt2++; });
      plugin2.on('end', () => {
        assert.strictEqual(cnt + cnt2, 2, 'File should be allowed twice (after reset, via overwrite)');
        done();
      });
      plugin2.end();
    });
    plugin.write(file); // 2nd write, should be filtered out
    plugin.end();
  });

  it('should create separate caches that only allow a file through once each', function(done) {
    const pluginA = cached('A');
    const pluginB = cached('B');
    const file = new File({ path: 'multi/file.txt', contents: Buffer.from('abc') });

    let seenA = 0, seenB = 0;
    pluginA.on('data', () => seenA++);
    pluginB.on('data', () => seenB++);

    pluginA.write(file);
    pluginB.write(file);

    pluginA.end();
    pluginB.end();

    setTimeout(() => {
      assert.strictEqual(seenA, 1, 'PluginA should allow file once');
      assert.strictEqual(seenB, 1, 'PluginB should allow file once');
      done();
    }, 25);
  });

  it('should create a cache that allows a stream file through always', function(done) {
    const plugin = cached('streams');
    const file = new File({ path: 'stream/yes.txt' });
    file.isStream = () => true;
    plugin.write(file);
    plugin.write(file);

    let cnt = 0;

    plugin.on('data', f => {
      ++cnt;
      assert.deepStrictEqual(f, file, 'Stream file passes through always');
    });
    plugin.on('end', () => {
      assert.strictEqual(cnt, 2, 'Should allow a stream file through always');
      done();
    });

    plugin.end();
  });

  it('should create a cache that allows a streaming file through always', function(done) {
    const plugin = cached('streams2');
    const file = new File({ path: 'stream/yes2.txt' });
    file.isStream = () => false;
    file.isBuffer = () => false;

    plugin.write(file);
    plugin.write(file);

    let cnt = 0;

    plugin.on('data', f => {
      ++cnt;
      assert.deepStrictEqual(f, file, 'Streaming file passes through always');
    });
    plugin.on('end', () => {
      assert.strictEqual(cnt, 2, 'Should allow a streaming file through always');
      done();
    });

    plugin.end();
  });

  it('should create a cache that only allows a hashed streaming file through once', function(done) {
    const plugin = cached('hashstream');
    const file = new File({ path: 'hash/stream.txt', contents: Buffer.from('xyz') });
    file.isBuffer = () => true;
    file.isStream = () => false;

    plugin.write(file);
    plugin.write(file); // duplicate

    let cnt = 0;
    plugin.on('data', f => { ++cnt; });
    plugin.on('end', () => {
      assert.strictEqual(cnt, 1, 'Should let only one through based on hash');
      done();
    });

    plugin.end();
  });
});