// PATCH: Update test framework from 'mocha' + 'should' to 'jest'

const Koa = require('koa');
const request = require('supertest');
const route = require('../');
const sleep = ms => new Promise(res => setTimeout(res, ms));

describe('route', () => {
  it('should yield to downstream middleware', async () => {
    const app = new Koa();

    let called = false;

    app.use(route.get('/foo', (ctx, next) => next()));
    app.use(async (ctx) => called = true);

    await request(app.callback())
      .get('/foo')
      .expect(404);

    expect(called).toBe(true);
  });

  it('should ignore when path does not match', async () => {
    const app = new Koa();

    app.use(route.get('/nope', (ctx) => {
      ctx.body = 'fail';
    }));

    await request(app.callback())
      .get('/yep')
      .expect(404);
  });

  it('should ignore when method does not match', async () => {
    const app = new Koa();

    app.use(route.post('/hi', (ctx) => {
      ctx.body = 'fail';
    }));

    await request(app.callback())
      .get('/hi')
      .expect(404);
  });

  it('should match HEAD for GET', async () => {
    const app = new Koa();

    app.use(route.get('/head', (ctx) => {
      ctx.status = 201;
    }));

    await request(app.callback())
      .head('/head')
      .expect(201);
  });

  it('should allow "all"', async () => {
    const app = new Koa();

    let called = false;
    app.use(route.all('/bar', (ctx, next) => { called = true; ctx.status = 200; if(typeof next === 'function') return next(); }));

    await request(app.callback())
      .patch('/bar')
      .expect(200);

    expect(called).toBe(true);
  });

  describe('route params', () => {
    it('should be decoded', async () => {
      const app = new Koa();

      app.use(route.get('/package/:name', function(ctx, name){
        ctx.body = name;
      }));

      await request(app.callback())
        .get('/package/foo%20bar')
        .expect(200)
        .expect('foo bar');
    });

    it('should be null if not matched', async () => {
      const app = new Koa();

      app.use(route.get('/api/:resource/:id?', function(ctx, resource, id){
        ctx.body = (id == null ? 'null' : id);
      }));

      await request(app.callback())
        .get('/api/articles')
        .expect(200)
        .expect('null');
    });

    it('should use the given options', async () => {
      const app = new Koa();

      app.use(route.get('/api/:resource/:id/posts', function(ctx, resource, id){
        ctx.body = resource + '-' + id;
      }, { end: false }));

      await request(app.callback())
        .get('/api/book/123/posts')
        .expect(200)
        .expect('book-123');
    });
  });
});