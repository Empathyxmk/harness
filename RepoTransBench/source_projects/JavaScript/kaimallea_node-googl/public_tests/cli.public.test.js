// Public CLI test for node-googl - different data to validate help/version/options output

const { exec } = require('child_process');
const assert = require('assert');

describe('CLI public tests', function() {
  it('should print help when unknown argument provided', function(done) {
    exec('node cli.js --foobar', (err, stdout, stderr) => {
      // The expected output is to show usage/help if invalid arg given
      const helpText = stdout + stderr;
      assert(helpText.toLowerCase().includes('usage'), 'Should output help instructions with unknown argument');
      done();
    });
  });

  it('should show version with -v (alias)', function(done) {
    exec('node cli.js -v', (err, stdout, stderr) => {
      assert(/\d+\.\d+\.\d+/.test(stdout + stderr), 'Should output version number with -v');
      done();
    });
  });

  it('should mention "shorten" in help output', function(done) {
    exec('node cli.js --help', (err, stdout, stderr) => {
      const help = stdout + stderr;
      assert(help.toLowerCase().includes('shorten'), 'Help output should mention the "shorten" command or feature');
      done();
    });
  });
});