const test = require('tape');
const express = require('express');
const session = require('express-session');
const request = require('supertest');
const userRouter = require('./router');

function makeApp() {
  const app = express();
  app.use(express.json());
  // The router expects session, so add a minimal session middleware
  app.use(session({
    secret: 'test_secret',
    resave: false,
    saveUninitialized: true
  }));
  app.use('/', userRouter);
  return app;
}

test('GET /profile without user should 401', t => {
  const app = makeApp();
  request(app)
    .get('/profile')
    .expect(401)
    .expect(res => {
      t.ok(res.text.includes('User required'), 'Responds with message about User required');
    })
    .end(t.end);
});

test('GET /profile with req.user should 200', t => {
  const app = express();
  app.use((req, res, next) => { req.user = { name: 'Jean' }; next(); });
  app.use(userRouter);

  request(app)
    .get('/profile')
    .expect(200)
    .expect(res => {
      t.ok(res.text.includes('Jean'), 'Should respond something for authorized user');
    })
    .end(t.end);
});

test('GET /profile with req.session.user should 200', t => {
  const app = express();
  app.use(express.json());
  app.use(session({
    secret: 'test_secret2',
    resave: false,
    saveUninitialized: true
  }));
  app.use((req, res, next) => { req.session.user = { name: 'Bob' }; next(); });
  app.use(userRouter);

  request(app)
    .get('/profile')
    .expect(200)
    .expect(res => {
      t.ok(res.text.includes('Bob'), 'Should respond something for authorized user');
    })
    .end(t.end);
});