const Koa = require('koa');
const request = require('supertest');
const route = require('../');
const sleep = ms => new Promise(res => setTimeout(res, ms));

describe('PUBLIC route', () => {
  it('should yield to downstream middleware (different path)', async () => {
    const app = new Koa();

    let called = false;

    app.use(route.get('/public', (ctx, next) => next()));
    app.use(async (ctx) => called = true);

    await request(app.callback())
      .get('/public')
      .expect(404);

    expect(called).toBe(true);
  });

  it('should ignore when path does not match (different path)', async () => {
    const app = new Koa();

    app.use(route.get('/notthis', (ctx) => {
      ctx.body = 'fail';
    }));

    await request(app.callback())
      .get('/anotherpath')
      .expect(404);
  });

  it('should ignore when method does not match (PUT instead of POST/GET)', async () => {
    const app = new Koa();

    app.use(route.put('/hi', (ctx) => {
      ctx.body = 'fail';
    }));

    await request(app.callback())
      .get('/hi')
      .expect(404);
  });

  it('should match HEAD for GET (different path)', async () => {
    const app = new Koa();

    app.use(route.get('/checkhead', (ctx) => {
      ctx.status = 204;
    }));

    await request(app.callback())
      .head('/checkhead')
      .expect(204);
  });

  it('should allow "all" (different method)', async () => {
    const app = new Koa();

    let called = false;
    app.use(route.all('/pub', (ctx, next) => { called = true; ctx.status = 201; if(typeof next === 'function') return next(); }));

    await request(app.callback())
      .delete('/pub')
      .expect(201);

    expect(called).toBe(true);
  });

  describe('route params (PUBLIC version)', () => {
    it('should be decoded (with different encoded value)', async () => {
      const app = new Koa();

      app.use(route.get('/city/:name', function(ctx, name){
        ctx.body = name;
      }));

      await request(app.callback())
        .get('/city/new%20york')
        .expect(200)
        .expect('new york');
    });

    it('should be null if not matched (changed path)', async () => {
      const app = new Koa();

      app.use(route.get('/api2/:type/:index?', function(ctx, type, index){
        ctx.body = (index == null ? 'null' : index);
      }));

      await request(app.callback())
        .get('/api2/widgets')
        .expect(200)
        .expect('null');
    });

    it('should use the given options (different params)', async () => {
      const app = new Koa();

      app.use(route.get('/api2/:category/:ref/items', function(ctx, category, ref){
        ctx.body = category + ':' + ref;
      }, { end: false }));

      await request(app.callback())
        .get('/api2/fruits/999/items')
        .expect(200)
        .expect('fruits:999');
    });
  });
});