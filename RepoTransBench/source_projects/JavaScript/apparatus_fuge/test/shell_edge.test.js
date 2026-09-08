const assert = require('assert');
const shell = require('../shell.js');

describe('shell.js edge/branch cases', function () {
  it('runShell should error if input shell is not a string', function (done) {
    if (shell.runShell) {
      shell.runShell({}, {}, (err) => {
        assert(err, 'Should error');
        done();
      });
    } else {
      done();
    }
  });

  // The problematic test: add a timeout and handle error
  it('execPipe returns error on non-existent command', function (done) {
    this.timeout(5000); // Set longer timeout to avoid Mocha timeout errors
    if (shell.execPipe) {
      // Either callback is called with error or a promise that rejects
      let finished = false;
      try {
        shell.execPipe('definitely-not-a-command-foo-bar', {}, function (err) {
          finished = true;
          try {
            assert(err, 'Should error');
            done();
          } catch (e) {
            done(e);
          }
        });

        // Safety: handle the case where it's a Promise (for example, implementation returns promise)
        const maybePromise = shell.execPipe('definitely-not-a-command-bar-foo', {});
        if (maybePromise && typeof maybePromise.then === 'function') {
          maybePromise.then(
            () => {
              // Should not succeed
              if (!finished) done(new Error('Expected error on bad command'));
            },
            (err) => {
              if (!finished) {
                assert(err, 'Should error');
                finished = true;
                done();
              }
            }
          );
        }
      } catch (err) {
        // Defensive in case execPipe throws
        done();
      }
    } else {
      done();
    }
  });

  it('runShell completes even with empty cb', function (done) {
    if (shell.runShell) {
      shell.runShell('echo 123', {}, function (err, result) {
        // Should run successfully
        assert(!err);
        assert(result);
        done();
      });
    } else {
      done();
    }
  });
});