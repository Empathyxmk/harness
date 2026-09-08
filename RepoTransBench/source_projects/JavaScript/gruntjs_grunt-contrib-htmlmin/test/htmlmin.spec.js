const path = require('path');
const fs = require('fs');
const mock = require('mock-fs');

describe('htmlmin Grunt task', () => {
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

    // Patch the minifier if needed
    if (errorOnMinify) {
      minifyMock = jest.fn(() => { throw new Error('Minify boom'); });
      minifierMocked = true;
    } else {
      minifyMock = jest.fn((src) => src.replace(/\s+/g, ' '));
      minifierMocked = true;
    }
    jest.resetModules();
    jest.doMock('html-minifier', () => ({ minify: minifyMock }));
    // Patch pretty-bytes and chalk too
    prettyBytesMock = jest.fn(() => 'Xb');
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

  test('minifies a valid HTML file with default options', () => {
    const srcFile = path.resolve('test/fixtures/test.html');
    const dest = path.resolve('tmp/test-spec-min.html');
    const HTML = '<html>\n   <body>   test </body> </html>';
    const filesArr = [{ src: [srcFile], dest }];
    const fakeGrunt = createFakeGrunt({ fileContents: { [srcFile]: HTML } });
    htmlmin(fakeGrunt);
    // Set up task context (as Grunt does)
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

  test('handles missing source file gracefully (src empty)', () => {
    const filesArr = [{ src: [], dest: 'tmp/none.html' }];
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
    expect(fakeGrunt.file.exists('tmp/none.html')).toBe(false);
  });

  test('warns and skips minifying when minifier throws', () => {
    const srcFile = 'test/fixtures/test.html';
    const filesArr = [{ src: [srcFile], dest: 'tmp/should-not-exist.html' }];
    const HTML = '<body> </body>';
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
    expect(warnMessages.join('\n')).toMatch(/test\.html[\s\S]*Minify boom/);
    expect(fakeGrunt.file.exists('tmp/should-not-exist.html')).toBe(false);
  });

  test('outputs count of successful and failed files', () => {
    const src = 'test/fixtures/test.html';
    const filesArr = [
      { src: [src], dest: 'tmp/success.html' },
      { src: [], dest: 'tmp/fail.html' }
    ];
    const fakeGrunt = createFakeGrunt({ fileContents: { [src]: '<h1> foo </h1> ' } });
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
    expect(fakeGrunt.file.exists('tmp/success.html')).toBe(true);
    expect(fakeGrunt.file.exists('tmp/fail.html')).toBe(false);
  });

  test('correctly applies minifier options', () => {
    const srcFile = path.resolve('test/fixtures/test.html');
    const dest = path.resolve('tmp/test-opt.html');
    const HTML = '<span>opt</span>';
    const filesArr = [{ src: [srcFile], dest }];
    const minifierOptions = { collapseWhitespace: true, removeComments: true };
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