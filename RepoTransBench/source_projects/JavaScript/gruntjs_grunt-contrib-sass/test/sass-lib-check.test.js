const path = require('path');

jest.mock('chalk', () => ({
  cyan: jest.fn((s) => s),
  red: jest.fn((s) => s),
  green: jest.fn((s) => s)
}));
jest.mock('dargs', () => jest.fn(() => ['--mocked']));
jest.mock('async', () => {
  const actual = jest.requireActual('async'); // For real series()
  return {
    ...actual,
    eachLimit: jest.fn((files, concurrency, iteratorFn, done) => {
      let idx = 0;
      function next() {
        if (idx < files.length) {
          iteratorFn(files[idx++], next)
        } else {
          done();
        }
      }
      next();
    })
  };
});
jest.mock('cross-spawn', () => jest.fn(() => ({
  on: function (event, cb) {
    if (event === 'close') {
      setTimeout(() => cb(0), 10); // Always "success"
    }
    return this;
  }
})));
jest.mock('grunt', () => ({
  file: {
    exists: jest.fn(() => true),
  },
  verbose: {
    writeln: jest.fn(),
    ok: jest.fn()
  },
  log: {
    ok: jest.fn(),
    error: jest.fn()
  },
  warn: jest.fn()
}));

const grunt = require('grunt');
const checkFilesSyntax = require('../tasks/lib/check');

describe('tasks/lib/check.js', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call ok when all files pass', (done) => {
    const files = ['test/test1.scss', 'test/test2.scss', '_partial.scss'];
    let okCalled = false;
    grunt.log.ok.mockImplementation(() => { okCalled = true; });
    checkFilesSyntax(files, {concurrencyCount: 2}, () => {
      expect(grunt.log.ok).toHaveBeenCalled();
      expect(grunt.warn).not.toHaveBeenCalled();
      expect(okCalled).toBeTruthy();
      done();
    });
  });

  it('should call warn when a file fails', (done) => {
    const spawn = require('cross-spawn');
    // mock close handler to simulate error for 1 file
    let callNo = 0;
    spawn.mockImplementation(() => ({
      on(event, cb) {
        if (event === 'close') {
          // First file: simulate error code>0
          setTimeout(() => cb(callNo++ === 0 ? 1 : 0), 10);
        }
        return this;
      }
    }));
    const files = ['test/test1.scss', 'test/test2.scss'];
    checkFilesSyntax(files, {concurrencyCount: 1}, () => {
      expect(grunt.warn).toHaveBeenCalled();
      done();
    });
  });
});