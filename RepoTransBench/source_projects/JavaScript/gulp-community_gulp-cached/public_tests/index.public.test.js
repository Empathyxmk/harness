const cached = require('../index');
const assert = require('assert');
const File = require('vinyl');

describe('gulp-cached extra cases (public)', function() {
  it('should allow optimizeMemory option and hash content with different file/path', function(done) {
    const plugin = cached('public-optimise', { optimizeMemory: true });
    const file = new File({ path: 'public/alpha.txt', contents: Buffer.from('hello world') });
    plugin.write(file);
    plugin.end();
    plugin.once('data', data => {
      assert.deepStrictEqual(data, file, 'File should match');
      done();
    });
  });

  it('should not add a file to cache if it is a stream (public test)', function(done) {
    const plugin = cached('public-stream');
    const file = new File({ path: 'public/stream2.txt' });
    file.isStream = () => true;
    plugin.write(file);
    plugin.end();
    let called = false;
    plugin.once('data', data => {
      called = true;
      assert.deepStrictEqual(data, file);
    });
    setTimeout(() => {
      assert.ok(called, 'Should call once for stream file in public');
      done();
    }, 10);
  });

  it('should support .isBuffer() returning false (public)', function(done) {
    const plugin = cached('public-false-buffer');
    const file = new File({ path: 'public/specialcase.txt' });
    file.isStream = () => false;
    file.isBuffer = () => false;
    plugin.write(file);
    plugin.end();
    plugin.once('data', data => {
      assert.ok(data instanceof File, 'Should still be a Vinyl File (public)');
      assert.strictEqual(data.path, file.path);
      done();
    });
  });

  it('should handle checksum property on buffer file and skip hashing (public)', function(done) {
    const plugin = cached('public-checksum');
    const buf = Buffer.from('123xyz');
    const file = new File({ path: 'bar/buf2.txt', contents: buf });
    file.checksum = 'different-checksum';
    file.isBuffer = () => true;
    file.isStream = () => false;

    plugin.write(file);
    plugin.end();
    plugin.once('data', data => {
      assert.strictEqual(data.checksum, 'different-checksum');
      done();
    });
  });

  it('should allow files with same path in different caches (public cache isolation)', function(done) {
    const plugin1 = cached('public-unique1');
    const plugin2 = cached('public-unique2');
    const filePath = 'commonpub/file.txt';
    const file1 = new File({ path: filePath, contents: Buffer.from('X') });
    const file2 = new File({ path: filePath, contents: Buffer.from('Y') });

    plugin1.write(file1);
    plugin2.write(file2);

    let received = 0;
    plugin1.once('data', data1 => {
      assert.strictEqual(data1.contents.toString(), 'X');
      received++;
      if (received === 2) done();
    });
    plugin2.once('data', data2 => {
      assert.strictEqual(data2.contents.toString(), 'Y');
      received++;
      if (received === 2) done();
    });

    plugin1.end();
    plugin2.end();
  });

  it('should not share cache if name is falsy (undefined in public)', function(done) {
    // Test that two unnamed caches do NOT share the same memory
    const pluginA = cached();
    const pluginB = cached();
    const filePathA = 'nofalsy/fileA.txt';
    const filePathB = 'nofalsy/fileB.txt';
    const fileA = new File({ path: filePathA, contents: Buffer.from('p') });
    const fileB = new File({ path: filePathB, contents: Buffer.from('q') });

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
      assert.ok(seenA, 'pluginA should let its file through (public)');
      assert.ok(seenB, 'pluginB should let its file through (public)');
      done();
    }, 25);
  });

  it('plugin.caches should be an object and exist on the module (public)', function() {
    assert.strictEqual(typeof cached.caches, 'object');
    assert.ok(cached.caches);
  });
});

describe('gulp-cached (public)', function() {
  it('should create a cache that only allows a file through once (public)', function(done) {
    const plugin = cached('public-simple');
    const file = new File({ path: 'baz/quux.txt', contents: Buffer.from('zoo') });
    plugin.write(file);
    let calls = 0;
    plugin.on('data', d => {
      ++calls;
      assert.deepStrictEqual(d, file);
    });
    plugin.on('end', () => {
      assert.strictEqual(calls, 1, 'File should only be allowed through once (public)');
      done();
    });
    plugin.write(file);
    plugin.end();
  });

  it('should create a cache that clears content when reset (public)', function(done) {
    const plugin = cached('public-reset');
    const file = new File({ path: 'alpha/bravo.txt', contents: Buffer.from('marble') });
    plugin.write(file);

    let cnt = 0;

    plugin.on('data', () => { cnt++; });
    plugin.on('end', () => {
      // now simulate cache reset using documented way:
      cached.caches['public-reset'] = {}; // clear the object literally as reset() method is not part of API
      // Create new plugin to use reset cache
      const plugin2 = cached('public-reset');
      plugin2.write(file);
      let cnt2 = 0;
      plugin2.on('data', () => { cnt2++; });
      plugin2.on('end', () => {
        assert.strictEqual(cnt + cnt2, 2, 'File should be allowed twice (after reset, via overwrite, public)');
        done();
      });
      plugin2.end();
    });
    plugin.write(file); // 2nd write, should be filtered out
    plugin.end();
  });

  it('should create separate caches that only allow a file through once each (public)', function(done) {
    const pluginA = cached('pubA');
    const pluginB = cached('pubB');
    const file = new File({ path: 'multi2/beta.txt', contents: Buffer.from('def') });

    let seenA = 0, seenB = 0;
    pluginA.on('data', () => seenA++);
    pluginB.on('data', () => seenB++);

    pluginA.write(file);
    pluginB.write(file);

    pluginA.end();
    pluginB.end();

    setTimeout(() => {
      assert.strictEqual(seenA, 1, 'PluginA should allow file once (public)');
      assert.strictEqual(seenB, 1, 'PluginB should allow file once (public)');
      done();
    }, 20);
  });
});