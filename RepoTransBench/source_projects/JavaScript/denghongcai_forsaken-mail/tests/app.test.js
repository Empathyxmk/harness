const request = require('supertest');

describe('Express App Structure', () => {
  let app;

  beforeEach(() => {
    jest.resetModules();
    app = require('../app');
  });

  test('GET /not-exist-path returns 404 with Not Found', async () => {
    const res = await request(app).get('/not-exist-path');
    expect(res.status).toBe(404);
    expect(res.text).toMatch(/Not Found/);
  });

  test('GET /api returns not 404 (API mount works)', async () => {
    const res = await request(app).get('/api');
    expect(res.status).not.toBe(404);
  });

  test('static file middleware is defined', async () => {
    expect(app._router.stack.some(layer => layer.name === 'serveStatic')).toBe(true);
  });

  // Instead of adding an error for a new route (which triggers only 404 middleware), we'll just test the standard error path for 404
});