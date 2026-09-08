// The package exports as { default: fn }, not as the fn itself, so adjust import.
const mod = require('../src/index');
const rollupCleanup = mod.default || mod;
const fs = require('fs');
const path = require('path');

describe('rollupCleanup', () => {
  it('should export a function', () => {
    expect(typeof rollupCleanup).toBe('function');
  });

  it('returns expected API', () => {
    const plugin = rollupCleanup({});
    expect(plugin).toHaveProperty('name');
    expect(plugin).toHaveProperty('transform');
  });

  it('runs transform and cleans up comments', async () => {
    const plugin = rollupCleanup({});
    const file = path.join(__dirname, 'fixtures', 'comments.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.code).not.toMatch(/\/\*/);
  });

  it('handles invalid code gracefully', async () => {
    const plugin = rollupCleanup({});
    const file = path.join(__dirname, 'fixtures', 'with_error.js');
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

  it('ignores non-included files', async () => {
    const plugin = rollupCleanup({ include: '**/*.foo' });
    const file = path.join(__dirname, 'fixtures', 'defaults.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result).toBeNull();
  });

  it('includes .foo files when extension set', async () => {
    const plugin = rollupCleanup({ extensions: ['.foo'] });
    const file = path.join(__dirname, 'fixtures', 'extensions.foo');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result).not.toBeNull();
    expect(result.code).not.toMatch(/\/\*/);
  });

  it('removes comments with specified regex', async () => {
    const plugin = rollupCleanup({ comments: /cleanup/i });
    const file = path.join(__dirname, 'fixtures', 'comments.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.code).not.toMatch(/cleanup/);
  });

  it('defaults to removing all comments', async () => {
    const plugin = rollupCleanup();
    const file = path.join(__dirname, 'fixtures', 'long_comment.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.code).not.toMatch(/\/\*/);
  });

  it('accepts options for sourcemaps', async () => {
    const plugin = rollupCleanup({ sourcemap: true });
    const file = path.join(__dirname, 'fixtures', 'defaults.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(result.map).toBeDefined();
  });

  it('passes with TS', async () => {
    const plugin = rollupCleanup({ extensions: ['.ts', '.js'] });
    const file = path.join(__dirname, 'fixtures', 'ts3s.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(typeof result.code).toBe('string');
  });

  it('does not modify es7 syntax', async () => {
    const plugin = rollupCleanup({ preserveFirstComment: true });
    const file = path.join(__dirname, 'fixtures', 'es7.js');
    const code = fs.readFileSync(file, 'utf8');
    const result = await plugin.transform(code, file);
    expect(typeof result.code).toBe('string');
  });

  it(
    'calls this.error when available and error has position',
    async () => {
      expect.assertions(2);

      let called = false;
      const fakeThis = {
        error: function (err) {
          called = true;
          // We want to ensure both assertions run, and expect(2) matches this count.
          expect(err.position).toBeDefined();
          throw err;
        },
      };

      const plugin = rollupCleanup({});
      const file = path.join(__dirname, 'fixtures', 'with_error.js');
      const code = fs.readFileSync(file, 'utf8');

      try {
        await plugin.transform.call(fakeThis, code, file);
      } catch (e) {
        // Should enter catch, after this.error is called
        expect(called).toBe(true);
      }
    },
    1500 // timeout
  );
});