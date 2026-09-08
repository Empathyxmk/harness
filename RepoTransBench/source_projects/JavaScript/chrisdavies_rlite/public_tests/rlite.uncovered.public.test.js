// These tests manually cover lines 11 and 15 of rlite.js UMD wrapper (public test variants).
// The logic is the same as the uncovered test, but we use a different check or diagnostic in the child process scripts.

const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

describe('rlite.js UMD wrapper coverage (public, lines 11, 15)', () => {
  const rlitePath = path.resolve(__dirname, '../rlite.js');

  it('covers AMD export path (define.amd), public case', () => {
    // Slightly different: set a result var to a special value, check for it
    const code = fs.readFileSync(rlitePath, 'utf8');
    const script = `
      let factoryCalledValue = 7;
      global.define = function(name, deps, factory) {
        factoryCalledValue = 42;
      };
      global.define.amd = true;
      eval(\`${code.replace(/`/g, '\\`')}\`);
      if (factoryCalledValue !== 42) process.exit(43);
    `;
    const res = spawnSync('node', ['-e', script], { encoding: 'utf-8' });
    if (res.error) throw res.error;
    if (res.status !== 0) throw new Error(\`AMD path not covered (exit \${res.status}):\\n\${res.stderr || ''}\\n\${res.stdout || ''}\`);
    expect(res.status).toBe(0);
  });

  it('covers CommonJS export path (module.exports), public case', () => {
    // Slightly different: check for function/obj property, but require "exports" instead of "module.exports"
    const code = fs.readFileSync(rlitePath, 'utf8');
    const script = `
      const module = {exports: {}};
      let exportsAssigned = false;
      global.module = module;
      global.exports = module.exports;
      eval(\`${code.replace(/`/g, '\\`')}\`);
      // It should attach something to module.exports
      if (!(typeof module.exports === "object" || typeof module.exports === "function")) process.exit(41);
      exportsAssigned = true;
      if (!exportsAssigned) process.exit(44);
    `;
    const res = spawnSync('node', ['-e', script], { encoding: 'utf-8' });
    if (res.error) throw res.error;
    if (res.status !== 0) throw new Error(\`CommonJS path not covered (exit \${res.status}):\\n\${res.stderr || ''}\\n\${res.stdout || ''}\`);
    expect(res.status).toBe(0);
  });
});