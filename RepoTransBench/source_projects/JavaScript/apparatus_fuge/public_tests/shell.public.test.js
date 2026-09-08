const assert = require('assert');
const shell = require('../shell.js');

describe('shell.js (public)', function () {
  it('exports expected keys (different check)', function () {
    const keys = Object.keys(shell);
    // Instead of array loop, test directly for keys (same logic, different)
    assert(keys.indexOf('execPipe') >= 0);
    assert(keys.indexOf('runShell') >= 0);
    assert(keys.indexOf('exec') >= 0);
  });

  it('runShell errors if input is not string (different type)', function (done) {
    if (shell.runShell) {
      try {
        shell.runShell(42, {}, (err) => {
          assert(err instanceof Error);
          done();
        });
      } catch (e) {
        assert(/must be a string/i.test(e.toString()));
        done();
      }
    } else {
      done(); // Not implemented, just pass
    }
  });

  it('exec returns error on obviously invalid command name', function (done) {
    if (shell.exec) {
      shell.exec('nonexistentpublicfoobarcmd', (err, stdout, stderr) => {
        assert(err || stderr);
        done();
      });
    } else {
      done();
    }
  });

  it('exec runs simple echo with different output', function (done) {
    if (shell.exec) {
      shell.exec('echo "barbaz"', (err, stdout, stderr) => {
        assert(!err);
        assert(stdout.includes('barbaz'));
        done();
      });
    } else {
      done();
    }
  });

  it('execPipe returns a promise and echo returns new value', async function() {
    if (typeof shell.execPipe === 'function') {
      const out = await shell.execPipe('echo "another pipe test"');
      assert('stdout' in out);
      assert(out.stdout.includes('another pipe test'));
    }
  });
});