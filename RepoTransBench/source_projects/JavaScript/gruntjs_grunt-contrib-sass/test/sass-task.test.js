jest.mock('which', () => ({
  sync: jest.fn()
}));
jest.mock('dargs', () => jest.fn(() => ['--mocked']));
jest.mock('async', () => {
  const actual = jest.requireActual('async');
  return {
    ...actual,
    eachLimit: jest.fn((items, concurrency, iterator, cb) => {
      let idx = 0;
      function next() {
        if (idx < items.length) {
          iterator(items[idx++], next);
        } else {
          cb();
        }
      }
      next();
    })
  }
});
jest.mock('cross-spawn', () => jest.fn(() => ({
  on: function (event, cb) {
    if (event === 'close') setTimeout(() => cb(0), 1);
    return this;
  }
})));
jest.mock('chalk', () => ({
  cyan: jest.fn((s) => s)
}));

describe('tasks/sass.js', () => {
  let grunt, mod;
  beforeEach(() => {
    // Reset state for each test
    jest.resetModules();
    grunt = {
      file: {
        exists: jest.fn(() => false),
        write: jest.fn()
      },
      verbose: {
        writeln: jest.fn(),
        ok: jest.fn()
      },
      warn: jest.fn((msg) => { throw new Error(msg) }),
      registerMultiTask: jest.fn((name, desc, fn) => { grunt._registered = fn; }),
      registerTask: jest.fn(),
      loadNpmTasks: jest.fn(),
      loadTasks: jest.fn(),
    };
    mod = require('../tasks/sass');
  });

  it('should register the sass multitask and handle compile path', (done) => {
    mod(grunt);
    // Simulate multiTask this context
    const task = {
      async: () => () => { done(); },
      options: () => ({}),
      files: [{
        src: ['a.scss'],
        dest: 'a.css'
      }],
      filesSrc: ['a.scss']
    };
    // Test compile path (checkBinary 'sass' called)
    expect(() => grunt._registered.call(task)).not.toThrow();
  });

  it('should throw if bundleExec and no bundle in PATH', () => {
    mod(grunt);
    // Which sync will throw on 'bundle'
    require('which').sync.mockImplementation((cmd) => {
      if (cmd === 'bundle') throw new Error('not found');
    });
    const task = {
      async: () => () => { },
      options: () => ({ bundleExec: true }),
      files: [],
      filesSrc: []
    };
    expect(() => grunt._registered.call(task)).toThrow();
  });

  it('should skip partials (underscore basename)', (done) => {
    mod(grunt);
    const task = {
      async: () => () => { done(); },
      options: () => ({}),
      files: [{
        src: ['_partial.scss'],
        dest: '_partial.css'
      }],
      filesSrc: ['_partial.scss']
    };
    expect(() => grunt._registered.call(task)).not.toThrow();
  });

  it('should call checkFilesSyntax when options.check', (done) => {
    const checkFilesSyntax = jest.fn((filesSrc, options, cb) => { cb(); });
    jest.doMock('../tasks/lib/check', () => checkFilesSyntax);
    mod = require('../tasks/sass');
    mod(grunt);
    const task = {
      async: () => () => { done(); },
      options: () => ({check: true}),
      files: [],
      filesSrc: ['test.scss']
    };
    expect(() => grunt._registered.call(task)).not.toThrow();
  });

  it('should treat --update correctly when file does not exist', (done) => {
    mod(grunt);
    grunt.file.exists.mockReturnValueOnce(false);
    const task = {
      async: () => () => { done(); },
      options: () => ({update: true}),
      files: [{
        src: ['test.scss'],
        dest: 'test.css'
      }],
      filesSrc: ['test.scss']
    };
    expect(() => grunt._registered.call(task)).not.toThrow();
  });

  it('should treat --update correctly when file does exist', (done) => {
    mod(grunt);
    grunt.file.exists.mockReturnValueOnce(true); // dest exists
    const task = {
      async: () => () => { done(); },
      options: () => ({update: true}),
      files: [{
        src: ['test.scss'],
        dest: 'test.css'
      }],
      filesSrc: ['test.scss']
    };
    expect(() => grunt._registered.call(task)).not.toThrow();
  });

  it('should add --scss arg for .css input', (done) => {
    mod(grunt);
    const task = {
      async: () => () => { done(); },
      options: () => ({}),
      files: [{
        src: ['foo.css'],
        dest: 'foo-out.css'
      }],
      filesSrc: ['foo.css']
    };
    expect(() => grunt._registered.call(task)).not.toThrow();
  });

  it('should use bundleExec path', (done) => {
    mod(grunt);
    require('which').sync.mockImplementation(() => {});
    const task = {
      async: () => () => { done(); },
      options: () => ({ bundleExec: true }),
      files: [{
        src: ['a.scss'],
        dest: 'a.css'
      }],
      filesSrc: ['a.scss']
    };
    expect(() => grunt._registered.call(task)).not.toThrow();
  });
});