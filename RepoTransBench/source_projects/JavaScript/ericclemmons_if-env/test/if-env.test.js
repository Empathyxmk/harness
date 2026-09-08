const { spawnSync } = require('child_process');
const path = require('path');
const assert = require('chai').assert;

const binPath = path.resolve(__dirname, '../bin/if-env.js');

describe('if-env CLI', function () {
  it('should exit 0 if environment variables match', function () {
    const result = spawnSync('node', [binPath, 'FOO=bar'], {
      env: Object.assign({}, process.env, { FOO: 'bar' }),
    });
    assert.strictEqual(result.status, 0, 'Should exit 0 when env matches');
  });

  it('should exit 1 if environment variable does not match', function () {
    const result = spawnSync('node', [binPath, 'FOO=wrong'], {
      env: Object.assign({}, process.env, { FOO: 'bar' }),
    });
    assert.strictEqual(result.status, 1, 'Should exit 1 when env does not match');
  });

  it('should exit 0 if no conditions are given (always true)', function () {
    const result = spawnSync('node', [binPath], {
      env: process.env,
    });
    assert.strictEqual(result.status, 0, 'Should exit 0 when no conditions');
  });

  it('should handle multiple conditions with all matching', function () {
    const result = spawnSync('node', [binPath, 'FOO=bar', 'BAZ=quux'], {
      env: Object.assign({}, process.env, { FOO: 'bar', BAZ: 'quux' }),
    });
    assert.strictEqual(result.status, 0);
  });

  it('should exit 1 if one of multiple conditions fails', function () {
    const result = spawnSync('node', [binPath, 'FOO=bar', 'BAZ=fail'], {
      env: Object.assign({}, process.env, { FOO: 'bar', BAZ: 'quux' }),
    });
    assert.strictEqual(result.status, 1);
  });

  it('should handle environment variables not defined (should fail)', function () {
    const result = spawnSync('node', [binPath, 'MISSING=anything'], {
      env: Object.assign({}, process.env),
    });
    assert.strictEqual(result.status, 1);
  });

  it('should handle empty value comparison (variable defined as empty string)', function () {
    const result = spawnSync('node', [binPath, 'FOO='], {
      env: Object.assign({}, process.env, { FOO: '' }),
    });
    assert.strictEqual(result.status, 0);
  });

  it('should treat absent variable and empty string as different', function () {
    // MISSING is not set in env, expected value is ''
    const result = spawnSync('node', [binPath, 'MISSING='], {
      env: Object.assign({}, process.env),
    });
    assert.strictEqual(result.status, 1);
  });
});