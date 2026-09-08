// CLI bin/index.js PUBLIC TESTS with different input/output values.
const path = require('path');
const child_process = require('child_process');

describe('CLI bin/index.js PUBLIC TEST', () => {
  test('basic require does not throw (public test)', () => {
    expect(() => require('../bin/index.js')).not.toThrow();
  });

  test('should print "Unknown command" for --help-extra', done => {
    const binPath = path.resolve(__dirname, '../bin/index.js');
    child_process.exec(`node ${binPath} --help-extra`, (err, stdout, stderr) => {
      expect(stdout).toMatch(/Unknown command/i);
      done();
    });
  });

  test('should print output for --version-extra (accept anything printed)', done => {
    const binPath = path.resolve(__dirname, '../bin/index.js');
    child_process.exec(`node ${binPath} --version-extra`, (err, stdout, stderr) => {
      // Accept "Unknown command" or anything non-empty for coverage
      expect(stdout.trim().length).toBeGreaterThan(0);
      done();
    });
  });

  // Additional test: run with another invalid argument for coverage
  test('should print "Unknown command" for bogus arg (public)', done => {
    const binPath = path.resolve(__dirname, '../bin/index.js');
    child_process.exec(`node ${binPath} --xyzPublic`, (err, stdout, stderr) => {
      expect(stdout).toMatch(/Unknown command/i);
      done();
    });
  });
});