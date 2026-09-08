// Duplicate and adapt the test/index.js to make it compatible with Jest, so it gets recognized and executed under Jest.
// (Jest recognizes *.test.js, and helps with coverage and result output.)

'use strict'

const request = require('supertest')
const assert = require('assert')
const serve = require('..')
const Koa = require('koa')

describe('serve(root)', function () {
  describe('when defer: false', function () {
    describe('when root = "."', function () {
      it('should serve from cwd', function (done) {
        const app = new Koa()
        app.use(serve('.'))
        request(app.listen())
          .get('/package.json')
          .expect(200, done)
      })
    })

    describe('when path is not a file', function () {
      it('should 404', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures'))
        request(app.listen())
          .get('/something')
          .expect(404, done)
      })

      it('should not throw 404 error', function (done) {
        const app = new Koa()
        let err = null
        app.use(async (ctx, next) => {
          try {
            await next()
          } catch (e) {
            err = e
          }
        })
        app.use(serve('test/fixtures'))
        app.use(async (ctx) => {
          ctx.body = 'ok'
        })
        request(app.listen())
          .get('/something')
          .expect(200)
          .end((_, res) => {
            assert.equal(res.text, 'ok')
            assert.equal(err, null)
            done()
          })
      })
    })

    describe('when upstream middleware responds', function () {
      it('should respond', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures'))
        app.use((ctx, next) => {
          return next().then(() => {
            ctx.body = 'hey'
          })
        })
        request(app.listen())
          .get('/hello.txt')
          .expect(200)
          .expect('world', done)
      })
    })

    describe('the path is valid', function () {
      it('should serve the file', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures'))
        request(app.listen())
          .get('/hello.txt')
          .expect(200)
          .expect('world', done)
      })
    })

    describe('.index', function () {
      describe('when present', function () {
        it('should alter the index file supported', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { index: 'index.txt' }))
          request(app.listen())
            .get('/')
            .expect(200)
            .expect('Content-Type', 'text/plain; charset=utf-8')
            .expect('text index', done)
        })
      })

      describe('when omitted', function () {
        it('should use index.html', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures'))
          request(app.listen())
            .get('/world/')
            .expect(200)
            .expect('Content-Type', 'text/html; charset=utf-8')
            .expect('html index', done)
        })
      })

      describe('when disabled', function () {
        it('should not use index.html', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { index: false }))
          request(app.listen())
            .get('/world/')
            .expect(404, done)
        })

        it('should pass to downstream if 404', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { index: false }))
          app.use(async (ctx) => {
            ctx.body = 'oh no'
          })
          request(app.listen())
            .get('/world/')
            .expect('oh no', done)
        })
      })
    })

    describe('when method is not `GET` or `HEAD`', function () {
      it('should 404', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures'))
        request(app.listen())
          .post('/hello.txt')
          .expect(404, done)
      })
    })
  })

  describe('when defer: true', function () {
    describe('when upstream middleware responds', function () {
      it('should do nothing', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures', { defer: true }))
        app.use((ctx, next) => {
          return next().then(() => {
            ctx.body = 'hey'
          })
        })
        request(app.listen())
          .get('/hello.txt')
          .expect(200)
          .expect('hey', done)
      })
    })

    describe('the path is valid', function () {
      it('should serve the file', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures', { defer: true }))
        request(app.listen())
          .get('/hello.txt')
          .expect(200)
          .expect('world', done)
      })
    })

    describe('when not valid', function () {
      it('should 404', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures', { defer: true }))
        request(app.listen())
          .get('/something')
          .expect(404, done)
      })

      it('should not throw 404 error', function (done) {
        const app = new Koa()
        let err = null
        app.use(async (ctx, next) => {
          try {
            await next()
          } catch (e) {
            err = e
          }
        })
        app.use(serve('test/fixtures', { defer: true }))
        app.use(async (ctx) => {
          ctx.body = 'ok'
        })
        request(app.listen())
          .get('/something')
          .expect(200)
          .end((_, res) => {
            assert.equal(res.text, 'ok')
            assert.equal(err, null)
            done()
          })
      })
    })

    describe('.index', function () {
      describe('when present', function () {
        it('should alter the index file supported', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { defer: true, index: 'index.txt' }))
          request(app.listen())
            .get('/')
            .expect(200)
            .expect('Content-Type', 'text/plain; charset=utf-8')
            .expect('text index', done)
        })
      })

      describe('when omitted', function () {
        it('should use index.html', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { defer: true }))
          request(app.listen())
            .get('/world/')
            .expect(200)
            .expect('Content-Type', 'text/html; charset=utf-8')
            .expect('html index', done)
        })
      })

      describe('when disabled', function () {
        it('should not use index.html', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { defer: true, index: false }))
          request(app.listen())
            .get('/world/')
            .expect(404, done)
        })

        it('should pass to downstream if 404', function (done) {
          const app = new Koa()
          app.use(serve('test/fixtures', { defer: true, index: false }))
          app.use(async (ctx) => {
            ctx.body = 'oh no'
          })
          request(app.listen())
            .get('/world/')
            .expect('oh no', done)
        })
      })
    })

    describe('when method is not `GET` or `HEAD`', function () {
      it('should 404', function (done) {
        const app = new Koa()
        app.use(serve('test/fixtures', { defer: true }))
        request(app.listen())
          .post('/hello.txt')
          .expect(404, done)
      })
    })
  })

  describe('root parameter', function () {
    it('should throw if root is missing', function () {
      expect(() => serve()).toThrow(/root directory is required to serve files/)
    })
  })
})