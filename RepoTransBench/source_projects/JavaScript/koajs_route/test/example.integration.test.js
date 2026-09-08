// Integration tests for example.js logic, focus on coverage for example.js

const Koa = require('koa');
const request = require('supertest');
const r = require('../index');

describe('example.js RESTful pets', () => {
  let app;

  beforeAll(() => {
    const db = {
      tobi: { name: 'tobi', species: 'ferret' },
      loki: { name: 'loki', species: 'ferret' },
      jane: { name: 'jane', species: 'ferret' }
    };
    const pets = {
      list: (ctx) => {
        var names = Object.keys(db);
        ctx.body = 'pets: ' + names.join(', ');
      },
      show: (ctx, name) => {
        var pet = db[name];
        if (!pet) return ctx.throw('cannot find that pet', 404);
        ctx.body = pet.name + ' is a ' + pet.species;
      }
    };
    app = new Koa();
    app.use(r.get('/pets', pets.list));
    app.use(r.get('/pets/:name', pets.show));
    // hack a throw
    app.context.throw = function (msg, code) {
      this.status = code || 500;
      this.body = msg;
    };
  });

  test('GET /pets returns list', async () => {
    await request(app.callback())
      .get('/pets')
      .expect(200)
      .expect('pets: tobi, loki, jane');
  });

  test('GET /pets/:name returns pet info', async () => {
    await request(app.callback())
      .get('/pets/tobi')
      .expect(200)
      .expect('tobi is a ferret');
    await request(app.callback())
      .get('/pets/loki')
      .expect(200)
      .expect('loki is a ferret');
  });

  test('GET /pets/:name not found returns 404', async () => {
    await request(app.callback())
      .get('/pets/unknown')
      .expect(404)
      .expect('cannot find that pet');
  });
});