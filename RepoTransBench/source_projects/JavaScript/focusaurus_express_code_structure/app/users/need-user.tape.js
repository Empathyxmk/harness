const test = require('tape');
const needUser = require('./need-user');

test('need-user should call next when req.user exists', t => {
  let called = false;
  const req = { user: { name: 'test' } };
  const res = {};
  needUser(req, res, function() {
    called = true;
    t.pass('next() called');
    t.end();
  });
  if (!called) t.fail('next() was not called');
});

test('need-user should call next when req.session.user exists', t => {
  let called = false;
  const req = { session: { user: { name: 'test' } } };
  const res = {};
  needUser(req, res, function() {
    called = true;
    t.pass('next() called');
    t.end();
  });
  if (!called) t.fail('next() was not called');
});

test('need-user should send 401 when no user/session present', t => {
  let sent = false;
  const req = {}; // no user, no session
  const res = {
    status: function(code) { t.equal(code, 401); return this; },
    send: function(msg) { sent = true; t.equal(msg, 'User required'); t.end(); }
  };
  needUser(req, res, function() {
    t.fail('next() should not be called');
    t.end();
  });
  setTimeout(() => { if (!sent) t.fail('send was not called'); }, 50);
});