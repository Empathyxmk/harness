const mod = require('../src/index');
const rollupCleanup = mod.default || mod;
const fs = require('fs');
const path = require('path');

describe('rollupCleanup public tests', () => {
  it('should export a function (public)', () => {
    expect(typeof rollupCleanup).toBe('function');
  });

  it('returns expected API (public)', () => {
    const plugin = rollupCleanup({ comments: 'license' });
    expect(plugin).toHaveProperty('name');
    expect(plugin).toHaveProperty('transform');
  });

  it('runs transform and cleans up custom file (public)', async () => {
    const plugin = rollupCleanup({});
    // Use a different fixture, e.g., 'defaults.js'
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'defaults.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.code).not.toMatch(/eslint/);
  });

  it('handles invalid code with different error file', async () => {
    const plugin = rollupCleanup({});
    // Use issue_10.js as another error-prone file
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'issue_10.js');
    const code = fs.readFileSync(file, 'utf8');
    let didThrow = false;
    try {
      await plugin.transform(code, file);
    } catch (err) {
      didThrow = true;
      expect(err).toBeInstanceOf(Error);
    }
    expect(didThrow).toBe(true);
  });

  it('ignores files not matching include pattern', async () => {
    const plugin = rollupCleanup({ include: '**/*.bar' });
    // defaults.js is .js, should be ignored now
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'defaults.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result).toBeNull();
  });

  it('includes .foo files with different extension config', async () => {
    const plugin = rollupCleanup({ extensions: ['.foo', '.bar'] });
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'extensions.foo');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result).not.toBeNull();
    expect(result.code).not.toMatch(/copyright/);
  });

  it('removes comments with a different regex', async () => {
    const plugin = rollupCleanup({ comments: /license/i });
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'comments.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.code).not.toMatch(/license/);
  });

  it('removes all comments from long_comment.js (public)', async () => {
    const plugin = rollupCleanup();
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'long_comment.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.code).not.toMatch(/TODO/);
  });

  it('accepts options for sourcemaps (public diff)', async () => {
    const plugin = rollupCleanup({ sourcemap: false });
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'comments.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    // Should be undefined since sourcemap: false
    expect(result.map).toBeUndefined();
  });

  it('passes with TS using another fixture', async () => {
    const plugin = rollupCleanup({ extensions: ['.js', '.ts'] });
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'ts3s.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(typeof result.code).toBe('string');
  });

  it('does not modify es7 syntax (public)', async () => {
    const plugin = rollupCleanup({ preserveFirstComment: false });
    const file = path.join(__dirname, '..', 'test', 'fixtures', 'es7.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(typeof result.code).toBe('string');
  });

  it(
    'calls this.error for different error (public)',
    async () => {
      expect.assertions(2);

      let called = false;
      const fakeThis = {
        error: function (err) {
          called = true;
          expect(typeof err.position).not.toBe('undefined');
          throw err;
        },
      };

      const plugin = rollupCleanup({});
      const file = path.join(__dirname, '..', 'test', 'fixtures', 'issue_11.js');
      const code = fs.readFileSync(file, 'utf8');

      try {
        await plugin.transform.call(fakeThis, code, file);
      } catch (e) {
        expect(called).toBe(true);
      }
    },
    1500
  );
});