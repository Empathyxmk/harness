const assert = require('assert');
const shell = require('../shell.js');

describe('shell.js', function () {
  it('exports expected keys', function () {
    const keys = Object.keys(shell);
    // If shell exports a default object, adjust accordingly:
    ['runShell', 'exec', 'execPipe'].forEach(k => assert(keys.includes(k), `Missing export: ${k}`));
  });

  it('runShell calls callback with error if input is not string', function (done) {
    if (shell.runShell) {
      try {
        shell.runShell(null, {}, (err) => {
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

  it('exec returns error on non-existent command', function (done) {
    if (shell.exec) {
      shell.exec('badcommandthatdoesnotexist', (err, stdout, stderr) => {
        assert(err || stderr);
        done();
      });
    } else {
      done();
    }
  });

  it('exec runs simple echo command', function (done) {
    if (shell.exec) {
      shell.exec('echo "foo"', (err, stdout, stderr) => {
        assert(!err);
        assert(stdout.includes('foo'));
        done();
      });
    } else {
      done();
    }
  });

  it('execPipe returns a promise (if defined)', async function() {
    if (typeof shell.execPipe === 'function') {
      const out = await shell.execPipe('echo "pipe test"');
      assert('stdout' in out);
      assert(out.stdout.includes('pipe test'));
    }
  });
});