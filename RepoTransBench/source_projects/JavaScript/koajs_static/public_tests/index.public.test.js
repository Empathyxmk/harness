'use strict';

// Public test variant for test/index.test.js with different test data

const request = require('supertest');
const assert = require('assert');
const serve = require('..');
const Koa = require('koa');
const path = require('path');

describe('PUBLIC: serve(root)', function () {
  describe('when defer: false', function () {
    describe('when root = "test/fixtures"', function () {
      it('should serve hello.txt', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures'));
        request(app.listen())
          .get('/hello.txt')
          .expect(200)
          .expect('world', done);
      });
    });

    describe('when path is not a file (file that does not exist)', function () {
      it('should 404', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures/world'));
        request(app.listen())
          .get('/nonexistentfile.html')
          .expect(404, done);
      });

      it('should not throw 404 error (with different file)', function (done) {
        const app = new Koa();
        let err = null;
        app.use(async (ctx, next) => {
          try {
            await next();
          } catch (e) {
            err = e;
          }
        });
        app.use(serve('test/fixtures/world'));
        app.use(async (ctx) => {
          ctx.body = 'ok-alt';
        });
        request(app.listen())
          .get('/nonexistentfile.html')
          .expect(200)
          .end((_, res) => {
            assert.equal(res.text, 'ok-alt');
            assert.equal(err, null);
            done();
          });
      });
    });

    describe('when upstream middleware responds (use /hello.txt which is a valid file so static does not respond)', function () {
      it('should respond', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures'));
        app.use((ctx, next) => {
          return next().then(() => {
            ctx.body = 'different-hey';
          })
        });
        // Instead of using an existing static file, use a file that DOES NOT EXIST so middleware responds
        request(app.listen())
          .get('/nonexistent-hey.txt')
          .expect(200)
          .expect('different-hey', done);
      });
    });

    describe('the path is valid (different file)', function () {
      it('should serve the file', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures'));
        request(app.listen())
          .get('/index.txt')
          .expect(200)
          .expect('text index', done);
      });
    });

    describe('.index', function () {
      describe('when present (use different index)', function () {
        it('should alter the index file supported', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world', { index: 'index.html' }));
          request(app.listen())
            .get('/')
            .expect(200)
            .expect('Content-Type', 'text/html; charset=utf-8')
            .expect('html index', done);
        });
      });

      describe('when omitted (different directory)', function () {
        it('should use index.html', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world'));
          request(app.listen())
            .get('/')
            .expect(200)
            .expect('Content-Type', 'text/html; charset=utf-8')
            .expect('html index', done);
        });
      });

      describe('when disabled (different directory)', function () {
        it('should not use index.html', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world', { index: false }));
          request(app.listen())
            .get('/')
            .expect(404, done);
        });

        it('should pass to downstream if 404', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world', { index: false }));
          app.use(async (ctx) => {
            ctx.body = 'oh no-alt';
          });
          request(app.listen())
            .get('/')
            .expect('oh no-alt', done);
        });
      });
    });

    describe('when method is not `GET` or `HEAD` (different file)', function () {
      it('should 404', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures/world'));
        request(app.listen())
          .post('/index.html')
          .expect(404, done);
      });
    });
  });

  describe('when defer: true', function () {
    describe('when upstream middleware responds (different file)', function () {
      it('should do nothing', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures', { defer: true }));
        app.use((ctx, next) => {
          return next().then(() => {
            ctx.body = 'hey-alt';
          });
        });
        // Use a nonexisting URI so static doesn't respond, and deferred middleware response applies
        request(app.listen())
          .get('/nonexistent-alt.txt')
          .expect(200)
          .expect('hey-alt', done);
      });
    });

    describe('the path is valid (different file)', function () {
      it('should serve the file', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures', { defer: true }));
        request(app.listen())
          .get('/index.txt')
          .expect(200)
          .expect('text index', done);
      });
    });

    describe('when not valid (different file)', function () {
      it('should 404', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures', { defer: true }));
        request(app.listen())
          .get('/no-such-file.txt')
          .expect(404, done);
      });

      it('should not throw 404 error (with different file)', function (done) {
        const app = new Koa();
        let err = null;
        app.use(async (ctx, next) => {
          try {
            await next();
          } catch (e) {
            err = e;
          }
        });
        app.use(serve('test/fixtures', { defer: true }));
        app.use(async (ctx) => {
          ctx.body = 'ok-defer-alt';
        });
        request(app.listen())
          .get('/no-such-file.txt')
          .expect(200)
          .end((_, res) => {
            assert.equal(res.text, 'ok-defer-alt');
            assert.equal(err, null);
            done();
          });
      });
    });

    describe('.index', function () {
      describe('when present (different index)', function () {
        it('should alter the index file supported', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures', { defer: true, index: 'index.txt' }));
          request(app.listen())
            .get('/')
            .expect(200)
            .expect('Content-Type', 'text/plain; charset=utf-8')
            .expect('text index', done);
        });
      });

      describe('when omitted (different directory)', function () {
        it('should use index.html', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world', { defer: true }));
          request(app.listen())
            .get('/')
            .expect(200)
            .expect('Content-Type', 'text/html; charset=utf-8')
            .expect('html index', done);
        });
      });

      describe('when disabled (different directory)', function () {
        it('should not use index.html', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world', { defer: true, index: false }));
          request(app.listen())
            .get('/')
            .expect(404, done);
        });

        it('should pass to downstream if 404', function (done) {
          const app = new Koa();
          app.use(serve('test/fixtures/world', { defer: true, index: false }));
          app.use(async (ctx) => {
            ctx.body = 'oh no-defer-alt';
          });
          request(app.listen())
            .get('/')
            .expect('oh no-defer-alt', done);
        });
      });
    });

    describe('when method is not `GET` or `HEAD` (different file)', function () {
      it('should 404', function (done) {
        const app = new Koa();
        app.use(serve('test/fixtures/world', { defer: true }));
        request(app.listen())
          .put('/index.html')
          .expect(404, done);
      });
    });
  });
});