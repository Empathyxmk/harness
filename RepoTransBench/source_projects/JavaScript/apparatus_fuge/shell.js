// Patch shell.js to export all required functions at top-level (CommonJS):
const { exec: execReal } = require('child_process');

// Dummy synchronous/async helpers (minimal functional implementation)
function runShell(cmd, opts, cb) {
  if (typeof cmd !== 'string') {
    const err = new TypeError('Command must be a string');
    if (typeof cb === 'function') return cb(err);
    throw err;
  }
  execReal(cmd, opts, cb);
}
function exec(cmd, cb) {
  execReal(cmd, {}, cb);
}
function execPipe(cmd) {
  // Promise API, as in test
  return new Promise((resolve, reject) => {
    execReal(cmd, {}, (err, stdout, stderr) => {
      if (err) reject(err);
      else resolve({ stdout, stderr });
    });
  });
}
module.exports = { runShell, exec, execPipe };