// PUBLIC unit tests for index.js using different paths/methods/params/data

const route = require('../index');

describe('PUBLIC index.js utility & internals', () => {
  test('should create a route function with custom method and options (different route)', async () => {
    const fn = jest.fn((ctx, product, next) => {
      if (typeof next === 'function') { return next(); }
    });
    const wrapper = route.put('/shop/:product', fn, { end: false });
    const ctx = { method: 'PUT', path: '/shop/laptop' };
    const next = jest.fn();
    await wrapper(ctx, next);
    expect(fn).toHaveBeenCalledWith(ctx, 'laptop', next);
  });

  test('should decode URI params (different value)', () => {
    const val = 'hello%2Bworld';
    const decode = val => val ? decodeURIComponent(val) : undefined;
    expect(decode(val)).toBe('hello+world');
    expect(decode()).toBeUndefined();
  });

  test('should support HEAD when only GET is defined (public, different path)', async () => {
    const fn = jest.fn((ctx, next) => { if(typeof next === 'function') return next(); });
    const wrapper = route.get('/about', fn);
    const ctx = { method: 'HEAD', path: '/about' };
    const next = jest.fn();
    await wrapper(ctx, next);
    expect(fn).toHaveBeenCalledWith(ctx, next);
  });

  test('should fall through if method does not match (PUT vs GET)', async () => {
    const fn = jest.fn();
    const wrapper = route.put('/account', fn);
    const ctx = { method: 'GET', path: '/account' };
    const next = jest.fn(() => Promise.resolve('methodMiss'));
    const result = await wrapper(ctx, next);
    expect(fn).not.toHaveBeenCalled();
    expect(result).toBe('methodMiss');
  });

  test('should fall through if path does not match (public, different path)', async () => {
    const fn = jest.fn();
    const wrapper = route.get('/foo', fn);
    const ctx = { method: 'GET', path: '/bar' };
    const next = jest.fn(() => Promise.resolve('noMatch'));
    const result = await wrapper(ctx, next);
    expect(fn).not.toHaveBeenCalled();
    expect(result).toBe('noMatch');
  });

  test('all() should match all methods (public, different path/methods)', async () => {
    const fn = jest.fn((ctx, next) => { if(typeof next === 'function') return next(); });
    const allFn = route.all('/mega', fn);
    const methods = ['DELETE', 'OPTIONS', 'PUT'];
    await Promise.all(
      methods.map(async m => {
        const ctx = { method: m, path: '/mega' };
        const next = jest.fn();
        await allFn(ctx, next);
        expect(fn).toHaveBeenCalledWith(ctx, next);
      })
    );
  });

  test('route.del should be aliased to route.delete (public check)', () => {
    expect(route.del).toBe(route.delete);
  });

  test('composed usage with (path)(fn), public version', async () => {
    const fn = jest.fn((ctx, city, next) => {
      ctx.body = city || 'none';
      if(typeof next === 'function') return next();
    });
    const composed = route.get('/city/:city')(fn);
    const ctx = { method: 'GET', path: '/city/london' };
    const next = jest.fn();
    await composed(ctx, next);
    expect(ctx.body).toBe('london');
  });

  test('should handle params with special characters and decode correctly (public)', async () => {
    const fn = jest.fn((ctx, code) => {
      ctx.code = code;
    });
    const wrapper = route.get('/voucher/:code', fn);
    const special = 'SALE%20OFF%2F2024';
    const ctx = { method: 'GET', path: '/voucher/' + special };
    const next = jest.fn();
    await wrapper(ctx, next);
    expect(ctx.code).toBe('SALE OFF/2024');
  });
});