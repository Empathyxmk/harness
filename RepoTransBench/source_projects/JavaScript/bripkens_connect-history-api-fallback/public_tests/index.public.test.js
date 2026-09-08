const historyApiFallback = require('../lib/index');
const sinon = require('sinon');

function makeReq(opts) {
    opts = opts || {};
    return Object.assign({
        method: 'GET',
        headers: {},
        url: '/foo'
    }, opts);
}

describe('connect-history-api-fallback (public)', function() {
    describe('[GET] should take JSON preference into account (public data)', function() {
        it('should not rewrite when Accept prefers JSON and fallbackToIndex is false (public)', function() {
            const middleware = historyApiFallback({ fallbackToIndex: false });
            const req = makeReq({
                method: 'GET',
                url: '/api/v2024/data',
                headers: {
                    accept: 'application/json, text/plain, */*'
                }
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/api/v2024/data');
            expect(next.called).toEqual(true);
        });

        it('should rewrite when Accept does not prefer JSON and fallbackToIndex is true (public)', function() {
            const middleware = historyApiFallback();
            const req = makeReq({
                method: 'GET',
                url: '/new-public',
                headers: {
                    accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/index.html');
            expect(next.called).toEqual(true);
        });
    });

    describe('[HEAD] should take JSON preference into account (public data)', function() {
        it('should not rewrite on HEAD when JSON preferred (public)', function() {
            const middleware = historyApiFallback({ fallbackToIndex: false });
            const req = makeReq({
                method: 'HEAD',
                url: '/v3/public/lookup',
                headers: {
                    accept: 'application/json'
                }
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/v3/public/lookup');
            expect(next.called).toEqual(true);
        });

        it('should rewrite on HEAD when Accept does not prefer JSON (public)', function() {
            const middleware = historyApiFallback();
            const req = makeReq({
                method: 'HEAD',
                url: '/new/other/route',
                headers: {
                    accept: 'text/html'
                }
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/index.html');
            expect(next.called).toEqual(true);
        });
    });

    describe('should respect dot rule by default (public)', function() {
        it('should not rewrite request if url has dot character (public)', function() {
            const middleware = historyApiFallback();
            const req = makeReq({
                url: '/static/my.lib.js'
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/static/my.lib.js');
            expect(next.called).toEqual(true);
        });
        it('should not rewrite .well-known resource requests (public)', function() {
            const middleware = historyApiFallback();
            const req = makeReq({
                url: '/.well-known/acme-challenge/something'
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/.well-known/acme-challenge/something');
            expect(next.called).toEqual(true);
        });
    });

    // Custom rewrites - for this test, we need to use GET/head and Accept: 'text/html',
    // because rewrites match only if 'text/html' is preferred
    describe('should allow custom rewrites (public)', function() {
        it('uses first rewrite rule that matches (public)', function() {
            const middleware = historyApiFallback({
                dotRule: false,
                rewrites: [
                    { from: /^\/foo-abc$/, to: '/alt1/index.html' },
                    { from: /./, to: '/alt2-fallback.html' },
                ]
            });
            const req = makeReq({
                url: '/foo-abc',
                method: 'GET',
                headers: {
                    accept: 'text/html'
                }
            });
            const next = sinon.spy();
            middleware(req, null, next);
            // After middleware, req.url will be rewritten if Accept prefers HTML
            expect(req.url).toEqual('/alt1/index.html'); // Should match first rule
            expect(next.called).toEqual(true);
        });

        it('uses second rewrite rule otherwise (public)', function() {
            const middleware = historyApiFallback({
                dotRule: false,
                rewrites: [
                    { from: /^\/foo-abc$/, to: '/alt1/index.html' },
                    { from: /./, to: '/alt2-fallback.html' },
                ]
            });
            const req = makeReq({
                url: '/bar-does-not-match',
                method: 'GET',
                headers: {
                    accept: 'text/html'
                }
            });
            const next = sinon.spy();
            middleware(req, null, next);
            expect(req.url).toEqual('/alt2-fallback.html'); // Should match second rule
            expect(next.called).toEqual(true);
        });
    });
});