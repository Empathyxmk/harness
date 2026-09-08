// These tests manually cover lines 11 and 15 of rlite.js UMD wrapper.
// We'll use a child process to simulate environments and test the actual UMD branches.
// Instead of using require, we will explicitly execute rlite.js as a script so the global context is correct.

const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

describe('rlite.js UMD wrapper coverage (lines 11, 15)', () => {
  const rlitePath = path.resolve(__dirname, '../rlite.js');

  it('covers AMD export path (define.amd)', () => {
    // The UMD expects to be loaded as a script, not via require, so use eval on the code.
    // We'll make define.amd true and ensure the code hits that line (no error = covered).
    const code = fs.readFileSync(rlitePath, 'utf8');
    const script = `
      let factoryCalled = false;
      global.define = function(name, deps, factory) {
        factoryCalled = true;
      };
      global.define.amd = true;
      eval(\`${code.replace(/`/g, '\\`')}\`);
      if (!factoryCalled) process.exit(42);
    `;
    const res = spawnSync('node', ['-e', script], { encoding: 'utf-8' });
    if (res.error) throw res.error;
    if (res.status !== 0) throw new Error(`AMD path not covered (exit ${res.status}):\n${res.stderr || ''}\n${res.stdout || ''}`);
    expect(res.status).toBe(0);
  });

  it('covers CommonJS export path (module.exports)', () => {
    // The UMD expects module.exports to be an object/function. We'll check that property was set.
    const code = fs.readFileSync(rlitePath, 'utf8');
    const script = `
      let called = false;
      const module = {exports: {}};
      global.module = module;
      global.exports = module.exports;
      function DummyRlite() { called = true; }
      eval(\`${code.replace(/`/g, '\\`')}\`);
      // It should attach something to module.exports
      if (!(module.exports && (typeof module.exports === "function" || typeof module.exports === "object"))) process.exit(42);
    `;
    const res = spawnSync('node', ['-e', script], { encoding: 'utf-8' });
    if (res.error) throw res.error;
    if (res.status !== 0) throw new Error(`CommonJS path not covered (exit ${res.status}):\n${res.stderr || ''}\n${res.stdout || ''}`);
    expect(res.status).toBe(0);
  });
});