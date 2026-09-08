const test = require('tape');
const rfx = require('../source');

// Existing tests
test('rfx.rfx()', assert => {
  const msg = 'should augment with .rfx() method';

  const actual = typeof rfx.rfx;
  const expected = 'function';

  assert.same(actual, expected, msg);
  assert.end();
});

test('fx.rfx.signature', assert => {
  const msg = 'should augment with rfx.signature string';

  const actual = rfx`string`(() => {}).rfx.signature;
  const expected = 'string';

  assert.same(actual, expected, msg);
  assert.end();
});

test('rfx preserve props', assert => {
  const msg = 'should preserve props from original';

  const fx = rfx`test`({ foo: 'foo' });
  const actual = fx.foo;
  const expected = 'foo';

  assert.equal(actual, expected, msg);
  assert.end();
});

// Additional tests for higher coverage

test('rfx signature passes non-string values', assert => {
  const msg = 'should handle non-string signature values gracefully';

  const numericSigRfx = rfx(123)(function() {});
  assert.equal(numericSigRfx.rfx.signature, '123', msg);

  const objSignature = rfx({ foo: 'bar' })(function() {});
  assert.equal(objSignature.rfx.signature, '[object Object]', msg);

  assert.end();
});

test('returned subject is mutated with rfx property', assert => {
  const msg = 'should mutate provided object/function with .rfx';

  function fn() { return 42; }
  const result = rfx`foo`(fn);

  assert.equal(typeof result.rfx, 'function', msg);
  assert.equal(result.rfx.signature, 'foo', 'signature string assigned');
  assert.equal(result(), 42, 'original function preserved');

  assert.end();
});

test('rfx.rfx logs the signature correctly to console', assert => {
  const fx = rfx`consolecheck`(() => {});
  let logged;
  const oldLog = console.log;
  console.log = function(val) {
    logged = val;
  };

  fx.rfx();
  assert.equal(logged, 'consolecheck', 'logs correct signature for template');

  console.log = oldLog;
  assert.end();
});

test('module.exports.default is rfx', assert => {
  const imported = require('../source');
  assert.equal(imported, imported.default, 'module.exports.default is rfx');
  assert.end();
});

test('works as both template literal and regular function call', assert => {
  function subject() {}
  const lit = rfx`abc`(subject);
  const fnc = rfx('abc')(subject);

  assert.equal(lit.rfx.signature, fnc.rfx.signature, 'signatures match');

  assert.end();
});