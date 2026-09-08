const express = require('express');
const request = require('supertest');
const api = require('../routes/api');

const mkApp = () => {
  const app = express();
  app.use('/api', api);
  return app;
};

describe('routes/api.js', () => {
  test('GET /api returns json', async () => {
    const res = await request(mkApp()).get('/api');
    expect(res.status).toBe(200);
    expect(res.type).toMatch(/json/);
    expect(res.body).toHaveProperty('success', true);
  });
});