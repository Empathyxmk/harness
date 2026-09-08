const chai = require('chai');
const sinon = require('sinon');
const express = require('express');
const request = require('supertest');
const subject = require('../');
const assert = chai.assert;

describe('ded_express-limiter public edge & branch cases', function () {
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

  it('should call whitelist(req) and bypass middleware with different lookup', function (done) {
    const whitelist = sinon.stub().returns(true);
    const mw = limiter({ lookup: 'headers.x-real-ip', total: 2, expire: 500, whitelist }); // changed lookup/total/expire
    const spy = sinon.spy();
    const req = { headers: {'x-real-ip': '2.3.4.5'} }, res = {}, next = spy;
    mw(req, res, next);
    assert.isTrue(spy.called, 'next should be called');
    done();
  });

  it('should handle opts.lookup as string (not array) with query parameter', function (done) {
    limiter({
      path: '/x',
      method: 'post',
      lookup: 'query.user',
      total: 3, // different total
      expire: 700
    });
    app.post('/x', (req, res) => res.sendStatus(201));
    request(app)
      .post('/x')
      .query({ user: 'john' })
      .expect(201, done);
  });

  it('should use default onRateLimited with new path and two requests', function (done) {
    limiter({
      path: '/y',
      method: 'put',
      lookup: 'ip',
      total: 1,
      expire: 600
    });
    app.put('/y', (req, res) => res.sendStatus(200));
    request(app).put('/y').expect(200, () => {
      request(app).put('/y').expect(429).expect('Rate limit exceeded', done);
    });
  });

  it('should handle opts.onRateLimited override with new message', function (done) {
    const custom = sinon.stub().callsFake((req, res, next) => {
      res.status(429).send('public custom');
    });
    limiter({
      path: '/z',
      method: 'delete',
      lookup: 'ip',
      total: 2,
      expire: 800,
      onRateLimited: custom
    });
    app.delete('/z', (req, res) => res.sendStatus(204));
    // Trip the limit
    request(app).delete('/z').expect(204, () => {
      request(app).delete('/z').expect(204, () => {
        request(app).delete('/z').expect(429, /public custom/, done);
      });
    });
  });

  it('should not set headers if skipHeaders=true and limit reached on other endpoint', function (done) {
    limiter({
      path: '/skip2',
      method: 'get',
      lookup: 'ip',
      total: 1,
      expire: 520,
      skipHeaders: true
    });
    app.get('/skip2', (req, res) => res.sendStatus(200));
    request(app).get('/skip2').expect(200, () => {
      request(app).get('/skip2')
        .expect(429)
        .expect(res => {
          if ('x-ratelimit-limit' in res.header || 'x-ratelimit-remaining' in res.header) throw new Error('unexpected headers');
        })
        .end(done);
    });
  });

  it('should handle expired limit and reset with a different delay', function (done) {
    limiter({
      path: '/reset2',
      method: 'get',
      lookup: 'ip',
      total: 2,
      expire: 900
    });
    app.get('/reset2', (req, res) => res.sendStatus(200));
    request(app).get('/reset2').expect(200, () => {
      request(app).get('/reset2').expect(200, () => {
        // expiring the limit
        clock.tick(1000);
        request(app).get('/reset2').expect(200, done);
      });
    });
  });

  it('should handle ignoreErrors flag, passes error with different redis error message', function (done) {
    // Fakes an error from redis.get
    const brokenRedis = {
      get: (key, cb) => cb(new Error('public_fail')),
      set: (key, val, px, expire, cb) => cb && cb(null)
    };
    const mylimiter = subject(app, brokenRedis);
    app.post('/err2', mylimiter({
      path: '/err2',
      method: 'post',
      lookup: 'ip',
      total: 2,
      expire: 750,
      ignoreErrors: true
    }), (req, res) => res.send('ok2'));
    request(app).post('/err2').expect(200, done);
  });

  it('should handle opts.method/opts.path undefined and return middleware (lookup string changed)', function () {
    const mw = limiter({
      lookup: 'headers.x-custom-ip',
      total: 5,
      expire: 600
    });
    assert.isFunction(mw, 'middleware returned');
  });

  it('should support lookup as a function with a new req property', function (done) {
    limiter({
      path: '/func2',
      method: 'put',
      lookup: function(req, res, opts, next) {
        req.lim_ip = '6.7.8.9';
        opts.lookup = 'lim_ip';
        opts.total = 1;
        next();
      },
      total: 5,
      expire: 1000
    });
    app.put('/func2', (req, res) => res.sendStatus(200));
    request(app).put('/func2').expect(200, done);
  });

  it('should not allow negative limit.remaining (total 2, expire longer)', function (done) {
    redis.get = (key, cb) => cb(null, JSON.stringify({total:2,remaining:0,reset: Date.now()+2000}));
    limiter({
      path: '/neg2',
      method: 'get',
      lookup: 'ip',
      total: 2,
      expire: 2000
    });
    app.get('/neg2', (req, res) => res.sendStatus(200));
    request(app).get('/neg2').expect(429, done);
  });

});