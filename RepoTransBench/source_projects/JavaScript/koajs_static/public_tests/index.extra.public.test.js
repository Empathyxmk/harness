'use strict';

// Public test variant for test/index.extra.test.js with different test data

const assert = require('assert');
const Koa = require('koa');
const serve = require('../index');
const http = require('http');
const path = require('path');

describe('PUBLIC: Extra tests for serve()', () => {
  it('throws if root is not supplied (same check)', () => {
    // This logic can't really use different "data", only error message can be checked
    assert.throws(() => serve(), /root directory is required to serve files/);
  });

  it('sets opts.root absolute (different directory)', () => {
    let opts = {};
    // Use a different valid directory (use cwd as a variant)
    serve(process.cwd(), opts);
    assert.ok(opts.root);
    assert.ok(opts.root === process.cwd());
  });

  it('uses default index if none provided (different subdirectory)', (done) => {
    const app = new Koa();

    // Use /world/ directory, which has index.html, instead of 'test/fixtures'
    app.use(serve('test/fixtures/world'));
    const server = app.listen();

    const req = http.request({
      port: server.address().port,
      path: '/', // / should map to index.html in world/
      method: 'GET'
    }, res => {
      assert.strictEqual(res.statusCode, 200);
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        assert.ok(data.includes('html index'));
        server.close(() => done());
      });
    });
    req.end();
  });

  it('handles HEAD requests like GET (different file)', (done) => {
    const app = new Koa();

    // Use a different file "index.txt" for HEAD request
    app.use(serve('test/fixtures'));

    const server = app.listen();

    http.request({
      port: server.address().port,
      path: '/index.txt',
      method: 'HEAD'
    }, res => {
      assert.strictEqual(res.statusCode, 200);
      server.close(() => done());
    }).end();
  });
});