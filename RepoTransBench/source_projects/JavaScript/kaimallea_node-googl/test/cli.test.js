// Existing CLI test for node-googl
// The CLI requires network and often fails outside a configured environment.
// For stable testing here, we'll just check the usage/help text.

const { exec } = require('child_process');
const assert = require('assert');

describe('CLI basic usage', function() {
  it('should output help information when run with no args', function(done) {
    exec('node cli.js', (err, stdout, stderr) => {
      assert(stdout.includes('Usage:'), 'Output should include usage instructions');
      done();
    });
  });

  it('should output version with --version', function(done) {
    exec('node cli.js --version', (err, stdout, stderr) => {
      assert(stdout.match(/\d+\.\d+\.\d+/), 'Output should contain a version string');
      done();
    });
  });

  it('should output help with --help', function(done) {
    exec('node cli.js --help', (err, stdout, stderr) => {
      assert(stdout.match(/Options:/), 'Output should include Options section');
      done();
    });
  });
});