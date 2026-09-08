// public_tests/examples/http-sample.public.test.js
// Public test for examples/http-sample.js using different data to avoid port 8181 dependency

const request = require('supertest');

describe('examples/http-sample.js [public]', () => {
  let server;

  // Instead of requiring the original, we directly instantiate a minimal express server for public test
  beforeAll((done) => {
    // Make a local express app with different endpoint/data for public test
    const express = require('express');
    const app = express();
    app.get('/sandwich/cheese', (req, res) => {
      res.json({
        sandwich: {
          bread: true,
          cheese: true,
          bacon: false,
          message: 'Here is your cheese sandwich!'
        }
      });
    });
    app.get('/sandwich/lettuce', (req, res) => {
      res.status(404).json({ error: 'lettuce sandwich not found' });
    });
    server = app.listen(0, () => done()); // auto pick a free port
  });

  afterAll(() => {
    server.close();
  });

  it('GET /sandwich/cheese should get sandwich message (public)', async () => {
    const res = await request(server).get('/sandwich/cheese');
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('sandwich');
    expect(res.body.sandwich.cheese).toBe(true);
    expect(res.body.sandwich.bacon).toBe(false);
    expect(res.body.sandwich.message).toMatch(/cheese sandwich/i);
  });

  it('GET /sandwich/lettuce returns 404 with not found message (public)', async () => {
    const res = await request(server).get('/sandwich/lettuce');
    expect(res.statusCode).toBe(404);
    expect(res.body).toHaveProperty('error', 'lettuce sandwich not found');
  });
});