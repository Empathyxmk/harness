const path = require('path');
const fs = require('fs');
const mock = require('mock-fs');

describe('htmlmin Grunt task - Public Tests', () => {
  let htmlmin;
  let minifierMocked = false;
  let minifyMock;
  let prettyBytesMock;
  let chalkMock;
  let logMessages;
  let warnMessages;

  // Create a fake grunt.file interface that matches Grunt's essential methods
  function createFakeGrunt({ fileContents = {}, errorOnRead = false, errorOnMinify = false } = {}) {
    logMessages = [];
    warnMessages = [];

    if (errorOnMinify) {
      minifyMock = jest.fn(() => { throw new Error('Public Minifier Broken'); });
      minifierMocked = true;
    } else {
      // (Change: use a different minify logic from original, but equivalent effect)
      minifyMock = jest.fn((src) => src.replace(/ +/g, ''));
      minifierMocked = true;
    }
    jest.resetModules();
    jest.doMock('html-minifier', () => ({ minify: minifyMock }));
    // Patch pretty-bytes and chalk too
    prettyBytesMock = jest.fn(() => '99b');
    jest.doMock('pretty-bytes', () => prettyBytesMock);
    chalkMock = new Proxy(
      (x) => x,
      { get: () => (x) => x }
    );
    jest.doMock('chalk', () => chalkMock);

    const fakeGrunt = {
      file: {
        read(src) {
          if (errorOnRead) throw new Error('read error');
          if (!(src in fileContents)) throw new Error('file not found: ' + src);
          return fileContents[src];
        },
        write(dest, content) {
          fileContents[dest] = content;
        },
        exists(src) {
          return src in fileContents;
        }
      },
      log: { writeln: (msg) => logMessages.push(msg) },
      verbose: { writeln: jest.fn() },
      warn: (msg) => warnMessages.push(msg),
      registerMultiTask(name, desc, fn) {
        fakeGrunt._fn = fn;
      },
    };
    // Reload htmlmin with mocks
    htmlmin = require('../tasks/htmlmin.js');
    return fakeGrunt;
  }

  afterEach(() => {
    jest.resetModules();
    mock.restore && mock.restore();
  });

  test('minifies another valid HTML file with default options (public)', () => {
    const srcFile = path.resolve('test/fixtures/public_input.html');
    const dest = path.resolve('tmp/public-test-spec-min.html');
    const HTML = '<div>   <p>hello public</p>\n</div>';
    const filesArr = [{ src: [srcFile], dest }];
    const fakeGrunt = createFakeGrunt({ fileContents: { [srcFile]: HTML } });
    htmlmin(fakeGrunt);
    const context = {
      options: () => ({}),
      files: filesArr,
      log: fakeGrunt.log,
      verbose: fakeGrunt.verbose
    };
    fakeGrunt._fn.call(context);
    expect(logMessages.join('\n')).toMatch(/Minified 1 files/);
    expect(minifyMock).toHaveBeenCalledWith(HTML, {});
    expect(fakeGrunt.file.exists(dest)).toBe(true);
    expect(fakeGrunt.file.read(dest)).not.toEqual(HTML);
  });

  test('handles missing public source file gracefully (src empty)', () => {
    const filesArr = [{ src: [], dest: 'tmp/public-none.html' }];
    const fakeGrunt = createFakeGrunt();
    htmlmin(fakeGrunt);
    const context = {
      options: () => ({}),
      files: filesArr,
      log: fakeGrunt.log,
      verbose: fakeGrunt.verbose
    };
    fakeGrunt._fn.call(context);
    expect(logMessages.join('\n')).toMatch(/Minified 0 files/);
    expect(fakeGrunt.file.exists('tmp/public-none.html')).toBe(false);
  });

  test('warns and skips minifying when minifier throws (public)', () => {
    const srcFile = 'test/fixtures/public_input.html';
    const filesArr = [{ src: [srcFile], dest: 'tmp/public-should-not-exist.html' }];
    const HTML = '<header> error </header>';
    const fakeGrunt = createFakeGrunt({ fileContents: { [srcFile]: HTML }, errorOnMinify: true });
    htmlmin(fakeGrunt);
    const context = {
      options: () => ({}),
      files: filesArr,
      log: fakeGrunt.log,
      verbose: fakeGrunt.verbose,
      warn: fakeGrunt.warn
    };
    fakeGrunt._fn.call(context);
    expect(warnMessages.join('\n')).toMatch(/public_input\.html[\s\S]*Public Minifier Broken/);
    expect(fakeGrunt.file.exists('tmp/public-should-not-exist.html')).toBe(false);
  });

  test('outputs count of successful and failed files (public)', () => {
    const src = 'test/fixtures/public_input.html';
    const filesArr = [
      { src: [src], dest: 'tmp/public-success.html' },
      { src: [], dest: 'tmp/public-fail.html' }
    ];
    const fakeGrunt = createFakeGrunt({ fileContents: { [src]: '<table> doctype </table>' } });
    htmlmin(fakeGrunt);
    const context = {
      options: () => ({}),
      files: filesArr,
      log: fakeGrunt.log,
      verbose: fakeGrunt.verbose
    };
    fakeGrunt._fn.call(context);
    expect(logMessages[logMessages.length - 1]).toMatch(
      /Minified 1 files \(1 failed\)/
    );
    expect(fakeGrunt.file.exists('tmp/public-success.html')).toBe(true);
    expect(fakeGrunt.file.exists('tmp/public-fail.html')).toBe(false);
  });

  test('correctly applies different minifier options (public)', () => {
    const srcFile = path.resolve('test/fixtures/public_input.html');
    const dest = path.resolve('tmp/public-test-opt.html');
    const HTML = '<section>section-test</section>';
    const filesArr = [{ src: [srcFile], dest }];
    const minifierOptions = { minifyJS: true, decodeEntities: true };
    const fakeGrunt = createFakeGrunt({ fileContents: { [srcFile]: HTML } });
    htmlmin(fakeGrunt);
    const context = {
      options: () => (minifierOptions),
      files: filesArr,
      log: fakeGrunt.log,
      verbose: fakeGrunt.verbose
    };
    fakeGrunt._fn.call(context);
    expect(minifyMock).toHaveBeenCalledWith(HTML, minifierOptions);
    expect(fakeGrunt.file.exists(dest)).toBe(true);
  });
});