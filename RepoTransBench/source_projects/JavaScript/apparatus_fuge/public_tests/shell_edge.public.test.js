const assert = require('assert');
const shell = require('../shell');

describe('shell.js edge (public)', function () {
  it('runShell with callback handles empty string command', function (done) {
    if (typeof shell.runShell === 'function') {
      shell.runShell('', {}, (err, stdout, stderr) => {
        // Should succeed, but probably empty output
        assert(!err);
        assert(typeof stdout === 'string' || typeof stderr === 'string');
        done();
      });
    } else {
      done();
    }
  });

  it('exec empty command gives no error or expected output', function (done) {
    if (typeof shell.exec === 'function') {
      shell.exec('', (err, stdout, stderr) => {
        // Should not throw, but may or may not return error/stdout/stderr
        assert(typeof stdout === 'string');
        done();
      });
    } else {
      done();
    }
  });

  it('execPipe handles trivial command (ls .)', async function () {
    if (typeof shell.execPipe === 'function') {
      const res = await shell.execPipe('ls .');
      assert(res && typeof res.stdout === 'string');
    }
  });
});