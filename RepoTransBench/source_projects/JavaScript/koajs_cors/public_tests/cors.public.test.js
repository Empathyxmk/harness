const cors = require('../index');

function createCtx(method, origin, headers = {}) {
  return {
    method,
    get: (h) => {
      if (h.toLowerCase() === 'origin') return origin;
      return headers[h];
    },
    header: Object.assign({ origin }, headers),
    request: { header: Object.assign({ origin }, headers), method },
    set: function (k, v) { this._headers[k] = v; },
    vary: function () { },
    _headers: {},
    status: undefined
  };
}

describe('CORS middleware (public tests)', () => {
  it('should set default headers for new simple requests', async () => {
    const ctx = createCtx('GET', 'https://publicsite.example');
    const middleware = cors();
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('*');
    expect(called).toBeTruthy();
  });

  it('should set allow origin from a different options.origin string', async () => {
    const ctx = createCtx('GET', 'https://foo.public.example');
    const middleware = cors({ origin: 'https://foo.allowed.com' });
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('https://foo.allowed.com');
    expect(called).toBeTruthy();
  });

  it('should use options.origin as async function with new value', async () => {
    const ctx = createCtx('GET', 'https://async.public.origin');
    const middleware = cors({
      origin: async (ctxX) => ctxX.get('origin') ? ctxX.get('origin').replace('public', 'allowed') : undefined
    });
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('https://async.allowed.origin');
    // Vary header is only present if returned by cors, so check presence and string type (or undefined)
    if ('Vary' in ctx._headers) {
      expect(typeof ctx._headers['Vary']).toBe('string');
      // If set, should include "Origin"
      expect(ctx._headers['Vary']).toContain('Origin');
    }
    expect(called).toBeTruthy();
  });

  it('should skip if options.origin function returns empty string (falsy) and different value', async () => {
    const ctx = createCtx('GET', 'https://skipme.public');
    const middleware = cors({
      origin: (ctxX) => {
        if (ctxX.get('origin').includes('skipme')) return '';
        return 'https://other.com';
      }
    });
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Allow-Origin']).toBeUndefined();
    expect(called).toBeTruthy();
  });

  it('should join new array headers', async () => {
    // These headers are set only for preflight, not GET
    const ctx = createCtx('GET', 'https://arrayheader.public');
    const middleware = cors({ allowMethods: ['POST', 'PUT'], allowHeaders: ['X-Custom-Header', 'Content-Type'] });
    let called = false;
    await middleware(ctx, () => { called = true; });

    // No change for GET: Allow-Origin only
    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('*');
    expect(called).toBeTruthy();
  });

  it('should handle credentials true and * origin with different site', async () => {
    const ctx = createCtx('GET', 'https://another.public.origin');
    const middleware = cors({ origin: (ctx) => ctx.get('origin'), credentials: true });
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('https://another.public.origin');
    expect(ctx._headers['Access-Control-Allow-Credentials']).toBe('true');
    // Only check Vary if present
    if ('Vary' in ctx._headers) {
      expect(typeof ctx._headers['Vary']).toBe('string');
      expect(ctx._headers['Vary']).toContain('Origin');
    }
    expect(called).toBeTruthy();
  });

  it('should handle credentials as function with new origin', async () => {
    const ctx = createCtx('GET', 'https://credentials.public');
    const middleware = cors({
      origin: (ctxX) => ctxX.get('origin'),
      credentials: (ctxX) => ctxX.get('origin') === 'https://credentials.public'
    });
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('https://credentials.public');
    expect(ctx._headers['Access-Control-Allow-Credentials']).toBe('true');
    expect(called).toBeTruthy();
  });

  it('should handle exposeHeaders and secureContext with new values', async () => {
    const ctx = createCtx('GET', 'https://headers.public');
    const middleware = cors({ exposeHeaders: ['X-Public-Header'], secureContext: true });
    let called = false;
    await middleware(ctx, () => { called = true; });

    expect(ctx._headers['Access-Control-Expose-Headers']).toBe('X-Public-Header');
    expect(ctx._headers['Cross-Origin-Resource-Policy']).toBeUndefined(); // not set by default
    expect(called).toBeTruthy();
  });

  it('should set default headers even if Origin is missing (variant)', async () => {
    const ctx = createCtx('GET', undefined);
    const middleware = cors();
    let called = false;
    await middleware(ctx, () => { called = true; });

    // In koajs_cors, returns '*' if Origin missing
    expect(ctx._headers['Access-Control-Allow-Origin']).toBe('*');
    expect(called).toBeTruthy();
  });

  it('should call next and handle error when keepHeadersOnError=false (different error)', async () => {
    const ctx = createCtx('GET', 'https://errhandl.public');
    const middleware = cors();
    let error;
    await middleware(ctx, async () => { throw new Error('boom2'); }).catch(e => { error = e; });
    expect(error).toBeDefined();
    expect(error.message).toBe('boom2');
    // The implementation sets headers property to all response headers, check that Access-Control-Allow-Origin is present
    expect(error.headers).toBeDefined();
    expect(error.headers['Access-Control-Allow-Origin']).toBe('*');
  });

  it('should attach headers to error when keepHeadersOnError=true (different error)', async () => {
    const ctx = createCtx('GET', 'https://errkeephead.public');
    const middleware = cors({
      origin: (ctx) => ctx.get('origin'),
      keepHeadersOnError: true
    });
    let error;
    await middleware(ctx, async () => { throw new Error('publicerror'); }).catch(e => { error = e; });
    expect(error).toBeDefined();
    expect(error.message).toBe('publicerror');
    expect(error.headers).toBeDefined();
    expect(error.headers['Access-Control-Allow-Origin']).toBe('https://errkeephead.public');
  });

  describe('OPTIONS preflight (public)', () => {
    it('should handle missing Access-Control-Request-Method header for preflight', async () => {
      const ctx = createCtx('OPTIONS', 'https://publicpreflight.example');
      const middleware = cors({ origin: (ctx) => ctx.get('origin') });
      let called = false;
      await middleware(ctx, () => { called = true; });

      // Implementation sets no preflight CORS headers if the method is missing
      // (see: https://github.com/koajs/cors/blob/master/index.js) so Access-Control-Allow-Origin is only set if GET/POST/etc.
      // So for OPTIONS without Access-Control-Request-Method, NO CORS header is set.
      expect(ctx.status).toBeUndefined();
      expect(ctx._headers['Access-Control-Allow-Origin']).toBeUndefined();
      expect(ctx._headers['Access-Control-Allow-Methods']).toBeUndefined();
      // If Vary was set, it should be present
      // Do NOT assert Vary content here as CORS skips for preflight with no method header
      expect(called).toBeTruthy(); // should NOT short-circuit
    });

    it('should set preflight headers with different values', async () => {
      const ctx = createCtx('OPTIONS', 'https://preflight.public.com', {
        'Access-Control-Request-Method': 'DELETE',
        'Access-Control-Request-Headers': 'x-preflight-header,content-type',
        'Access-Control-Request-Private-Network': 'true'
      });
      const middleware = cors({
        origin: (ctx) => ctx.get('origin'),
        maxAge: 86400,
        allowMethods: ['DELETE', 'PUT'],
        allowHeaders: ['X-Preflight-Header', 'Content-Type'],
        privateNetworkAccess: true
      });
      let called = false;
      await middleware(ctx, () => { called = true; });

      // Implementation sets ctx.status = 204 if all preflight inputs present
      expect(ctx.status).toBe(204);
      expect(ctx._headers['Access-Control-Allow-Origin']).toBe('https://preflight.public.com');
      expect(ctx._headers['Access-Control-Allow-Methods']).toBe('DELETE,PUT');
      expect(ctx._headers['Access-Control-Allow-Headers']).toBe('X-Preflight-Header,Content-Type');
      // max-age expected as string
      expect(ctx._headers['Access-Control-Max-Age']).toBe('86400');
      // Private-Network test
      expect(ctx._headers['Access-Control-Allow-Private-Network']).toBe('true');
      // In preflight requests, next should not be called
      expect(called).toBeFalsy();
    });
  });
});