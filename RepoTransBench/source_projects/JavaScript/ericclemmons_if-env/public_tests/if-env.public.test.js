const { spawnSync } = require('child_process');
const path = require('path');
const assert = require('chai').assert;

const binPath = path.resolve(__dirname, '../bin/if-env.js');

describe('if-env CLI (public tests, different data)', function () {
  it('should exit 0 if environment variables match (public test)', function () {
    const result = spawnSync('node', [binPath, 'ABC=123'], {
      env: Object.assign({}, process.env, { ABC: '123' }),
    });
    assert.strictEqual(result.status, 0, 'Should exit 0 when env matches');
  });

  it('should exit 1 if environment variable does not match (public test)', function () {
    const result = spawnSync('node', [binPath, 'ABC=wrong'], {
      env: Object.assign({}, process.env, { ABC: '123' }),
    });
    assert.strictEqual(result.status, 1, 'Should exit 1 when env does not match');
  });

  it('should exit 0 if no conditions are given (always true) (public test)', function () {
    const result = spawnSync('node', [binPath], {
      env: process.env,
    });
    assert.strictEqual(result.status, 0, 'Should exit 0 when no conditions');
  });

  it('should handle multiple conditions with all matching (public test)', function () {
    const result = spawnSync('node', [binPath, 'ABC=123', 'XYZ=789'], {
      env: Object.assign({}, process.env, { ABC: '123', XYZ: '789' }),
    });
    assert.strictEqual(result.status, 0);
  });

  it('should exit 1 if one of multiple conditions fails (public test)', function () {
    const result = spawnSync('node', [binPath, 'ABC=123', 'XYZ=fail'], {
      env: Object.assign({}, process.env, { ABC: '123', XYZ: '789' }),
    });
    assert.strictEqual(result.status, 1);
  });

  it('should handle environment variables not defined (should fail, public test)', function () {
    const result = spawnSync('node', [binPath, 'UNSET=defined'], {
      env: Object.assign({}, process.env),
    });
    assert.strictEqual(result.status, 1);
  });

  it('should handle empty value comparison (variable defined as empty string, public test)', function () {
    const result = spawnSync('node', [binPath, 'ABC='], {
      env: Object.assign({}, process.env, { ABC: '' }),
    });
    assert.strictEqual(result.status, 0);
  });

  it('should treat absent variable and empty string as different (public test)', function () {
    const result = spawnSync('node', [binPath, 'UNSET='], {
      env: Object.assign({}, process.env),
    });
    assert.strictEqual(result.status, 1);
  });
});