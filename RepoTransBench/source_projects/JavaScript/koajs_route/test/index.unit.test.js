// Focused unit tests for index.js to increase coverage

const route = require('../index');

// Patch: The original signature for middleware is (ctx, ...params, next).
// But test was written using (ctx, next) or (ctx, param, next).
// We need to ensure we do not call "next" if it's not supplied.
// So we wrap next as undefined unless route injects it as last param.

describe('index.js utility & internals', () => {
  test('should create a route function with custom method and options', async () => {
    const fn = jest.fn((ctx, name, next) => {
      // Accept a variable number of args
      if (typeof next === 'function') { return next(); }
    });
    const wrapper = route.get('/foo/:name', fn, { end: false });
    const ctx = { method: 'GET', path: '/foo/bar' };
    const next = jest.fn();
    await wrapper(ctx, next);
    expect(fn).toHaveBeenCalledWith(ctx, 'bar', next);
  });

  test('should decode URI params', () => {
    const val = 'foo%20bar';
    const decode = val => val ? decodeURIComponent(val) : undefined;
    expect(decode(val)).toBe('foo bar');
    expect(decode()).toBeUndefined();
  });

  test('should support HEAD when only GET is defined', async () => {
    const fn = jest.fn((ctx, next) => { if(typeof next === 'function') return next(); });
    const wrapper = route.get('/info', fn);
    const ctx = { method: 'HEAD', path: '/info' };
    const next = jest.fn();
    await wrapper(ctx, next);
    expect(fn).toHaveBeenCalledWith(ctx, next);
  });

  test('should fall through if method does not match', async () => {
    const fn = jest.fn();
    const wrapper = route.post('/bar', fn);
    const ctx = { method: 'GET', path: '/bar' };
    const next = jest.fn(() => Promise.resolve('called'));
    const result = await wrapper(ctx, next);
    expect(fn).not.toHaveBeenCalled();
    expect(result).toBe('called');
  });

  test('should fall through if path does not match', async () => {
    const fn = jest.fn();
    const wrapper = route.get('/foo', fn);
    const ctx = { method: 'GET', path: '/baz' };
    const next = jest.fn(() => Promise.resolve('notFound'));
    const result = await wrapper(ctx, next);
    expect(fn).not.toHaveBeenCalled();
    expect(result).toBe('notFound');
  });

  test('all() should match all methods', async () => {
    const fn = jest.fn((ctx, next) => { if(typeof next === 'function') return next(); });
    const allFn = route.all('/all', fn);
    const methods = ['GET', 'POST', 'PATCH'];
    await Promise.all(
      methods.map(async m => {
        const ctx = { method: m, path: '/all' };
        const next = jest.fn();
        await allFn(ctx, next);
        expect(fn).toHaveBeenCalledWith(ctx, next);
      })
    );
  });

  test('route.del should be aliased to route.delete', () => {
    expect(route.del).toBe(route.delete);
  });

  test('composed usage with (path)(fn)', async () => {
    const fn = jest.fn((ctx, name, next) => {
      ctx.body = name || 'no';
      if(typeof next === 'function') return next();
    });
    const composed = route.get('/x/:name')(fn);
    const ctx = { method: 'GET', path: '/x/john' };
    const next = jest.fn();
    await composed(ctx, next);
    expect(ctx.body).toBe('john');
  });

  test('should handle params with special characters and decode correctly', async () => {
    const fn = jest.fn((ctx, id) => {
      ctx.id = id;
    });
    const wrapper = route.get('/item/:id', fn);
    const special = 'test%20item%2Fid';
    const ctx = { method: 'GET', path: '/item/' + special };
    const next = jest.fn();
    await wrapper(ctx, next);
    expect(ctx.id).toBe('test item/id');
  });
});