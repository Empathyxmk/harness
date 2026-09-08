const chai = require('chai');
const sinon = require('sinon');
const express = require('express');
const request = require('supertest');
const subject = require('../');
const assert = chai.assert;

describe('ded_express-limiter edge & branch cases', function () {
  let app, redis, limiter, clock;

  beforeEach(function () {
    // Use a simple in-memory replacement for redis with get/set
    const store = {};
    redis = {
      get: (key, cb) => cb(null, store[key]),
      set: (key, val, px, expire, cb) => {
        store[key] = val; if (typeof cb === 'function') cb(null);
      },
      flushdb: cb => { Object.keys(store).forEach(k => delete store[k]); if (cb) cb(); }
    };
    app = express();
    limiter = subject(app, redis);
    clock = sinon.useFakeTimers({ now: Date.now() });
  });

  afterEach(function () {
    clock.restore();
  });

  it('should call whitelist(req) and bypass middleware', function (done) {
    const whitelist = sinon.stub().returns(true);
    const mw = limiter({ lookup: 'ip', total: 1, expire: 1000, whitelist });
    const spy = sinon.spy();
    const req = { ip: '1.2.3.4' }, res = {}, next = spy;
    mw(req, res, next);
    assert.isTrue(spy.called, 'next should be called');
    done();
  });

  it('should handle opts.lookup as string (not array)', function (done) {
    limiter({
      path: '/a',
      method: 'get',
      lookup: 'ip',
      total: 2,
      expire: 1000
    });
    app.get('/a', (req, res) => res.sendStatus(200));
    request(app).get('/a').expect(200, done);
  });

  it('should use default onRateLimited', function (done) {
    limiter({
      path: '/b',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 1000
    });
    app.get('/b', (req, res) => res.sendStatus(200));
    request(app).get('/b').expect(200, () => {
      request(app).get('/b').expect(429).expect('Rate limit exceeded', done);
    });
  });

  it('should handle opts.onRateLimited override', function (done) {
    const custom = sinon.stub().callsFake((req, res, next) => {
      res.status(429).send('custom');
    });
    limiter({
      path: '/c',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 1000,
      onRateLimited: custom
    });
    app.get('/c', (req, res) => res.sendStatus(200));
    // Trip the limit
    request(app).get('/c').expect(200, () => {
      request(app).get('/c').expect(429, /custom/, done);
    });
  });

  it('should not set headers if skipHeaders=true and limit reached', function (done) {
    limiter({
      path: '/skip',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 1000,
      skipHeaders: true
    });
    app.get('/skip', (req, res) => res.sendStatus(200));
    // First call is ok
    request(app).get('/skip').expect(200, () => {
      // Second call triggers rate limit
      request(app).get('/skip')
        .expect(429)
        .expect(res => {
          if ('x-ratelimit-limit' in res.header || 'x-ratelimit-remaining' in res.header) throw new Error('unexpected headers');
        })
        .end(done);
    });
  });

  it('should handle expired limit and reset', function (done) {
    limiter({
      path: '/reset',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 1000
    });
    app.get('/reset', (req, res) => res.sendStatus(200));
    request(app).get('/reset').expect(200, () => {
      // expiring the limit
      clock.tick(1001);
      request(app).get('/reset').expect(200, done);
    });
  });

  it('should handle ignoreErrors flag, passes error to next()', function (done) {
    // Fakes an error from redis.get
    const brokenRedis = {
      get: (key, cb) => cb(new Error('fail')),
      set: (key, val, px, expire, cb) => cb && cb(null)
    };
    const mylimiter = subject(app, brokenRedis);
    app.get('/err', mylimiter({
      path: '/err',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 1000,
      ignoreErrors: true
    }), (req, res) => res.send('ok'));
    request(app).get('/err').expect(200, done);
  });

  it('should handle opts.method/opts.path undefined and return middleware', function () {
    const mw = limiter({
      lookup: 'ip',
      total: 1,
      expire: 1000
    });
    assert.isFunction(mw, 'middleware returned');
  });

  it('should support lookup as a function', function (done) {
    limiter({
      path: '/func',
      method: 'get',
      lookup: function(req, res, opts, next) {
        opts.lookup = 'ip';
        opts.total = 1;
        next();
      },
      total: 10,
      expire: 1000
    });
    app.get('/func', (req, res) => res.sendStatus(200));
    request(app).get('/func').expect(200, done);
  });

  it('should not allow negative limit.remaining', function (done) {
    // Prepare a pre-hit state, manually insert remaining = 0 into redis
    redis.get = (key, cb) => cb(null, JSON.stringify({total:1,remaining:0,reset: Date.now()+999}));
    limiter({
      path: '/neg',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 10000
    });
    app.get('/neg', (req, res) => res.sendStatus(200));
    request(app).get('/neg').expect(429, done);
  });
});