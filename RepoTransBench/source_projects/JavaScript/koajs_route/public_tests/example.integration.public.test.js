// Public integration tests for example.js logic, with different pet data

const Koa = require('koa');
const request = require('supertest');
const r = require('../index');

describe('PUBLIC example.js RESTful vehicles', () => {
  let app;

  beforeAll(() => {
    const db = {
      tesla: { name: 'tesla', type: 'car' },
      boeing: { name: 'boeing', type: 'plane' },
      yamaha: { name: 'yamaha', type: 'bike' }
    };
    const vehicles = {
      list: (ctx) => {
        var names = Object.keys(db);
        ctx.body = 'vehicles: ' + names.join(', ');
      },
      show: (ctx, name) => {
        var vehicle = db[name];
        if (!vehicle) return ctx.throw('cannot find that vehicle', 404);
        ctx.body = vehicle.name + ' is a ' + vehicle.type;
      }
    };
    app = new Koa();
    app.use(r.get('/vehicles', vehicles.list));
    app.use(r.get('/vehicles/:name', vehicles.show));
    // hack a throw
    app.context.throw = function (msg, code) {
      this.status = code || 500;
      this.body = msg;
    };
  });

  test('GET /vehicles returns list', async () => {
    await request(app.callback())
      .get('/vehicles')
      .expect(200)
      .expect('vehicles: tesla, boeing, yamaha');
  });

  test('GET /vehicles/:name returns vehicle info', async () => {
    await request(app.callback())
      .get('/vehicles/tesla')
      .expect(200)
      .expect('tesla is a car');
    await request(app.callback())
      .get('/vehicles/yamaha')
      .expect(200)
      .expect('yamaha is a bike');
  });

  test('GET /vehicles/:name not found returns 404 (public)', async () => {
    await request(app.callback())
      .get('/vehicles/unknown')
      .expect(404)
      .expect('cannot find that vehicle');
  });
});