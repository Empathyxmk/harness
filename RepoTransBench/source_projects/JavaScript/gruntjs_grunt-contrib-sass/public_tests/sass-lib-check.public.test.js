const path = require('path');

jest.mock('chalk', () => ({
  cyan: jest.fn((s) => s),
  red: jest.fn((s) => s),
  green: jest.fn((s) => s)
}));
jest.mock('dargs', () => jest.fn(() => ['--public-mocked']));
jest.mock('async', () => {
  const actual = jest.requireActual('async');
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
      setTimeout(() => cb(0), 5); // Always "success"
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

describe('tasks/lib/check.js (public test data)', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call ok when all PUBLIC files pass', (done) => {
    const files = ['public_test/a.scss', 'public_test/b.scss', '_component.scss'];
    let okCalled = false;
    grunt.log.ok.mockImplementation(() => { okCalled = true; });
    checkFilesSyntax(files, {concurrencyCount: 3}, () => {
      expect(grunt.log.ok).toHaveBeenCalled();
      expect(grunt.warn).not.toHaveBeenCalled();
      expect(okCalled).toBeTruthy();
      done();
    });
  });

  it('should call warn when a PUBLIC file fails', (done) => {
    const spawn = require('cross-spawn');
    // mock close handler to simulate error for 1 file - public data variant
    let callNo = 0;
    spawn.mockImplementation(() => ({
      on(event, cb) {
        if (event === 'close') {
          // First file: simulate error code>0
          setTimeout(() => cb(callNo++ === 0 ? 2 : 0), 5);
        }
        return this;
      }
    }));
    const files = ['public_test/foo.scss', 'public_test/bar.scss'];
    checkFilesSyntax(files, {concurrencyCount: 2}, () => {
      expect(grunt.warn).toHaveBeenCalled();
      done();
    });
  });
});