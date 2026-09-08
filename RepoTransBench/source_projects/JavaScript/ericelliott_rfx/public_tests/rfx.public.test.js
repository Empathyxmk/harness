const test = require('tape');
const rfx = require('../source');

// Public test using different signature string
test('public: rfx.rfx() exists as function', assert => {
  const msg = 'public: .rfx() function is present';
  assert.same(typeof rfx.rfx, 'function', msg);
  assert.end();
});

// Public test: different signature content
test('public: rfx.rfx.signature for "foobar"', assert => {
  const msg = 'public: assigns signature "foobar"';
  const actual = rfx`foobar`(() => {}).rfx.signature;
  const expected = 'foobar';
  assert.same(actual, expected, msg);
  assert.end();
});

// Public test: preserve different prop name and value
test('public: rfx preserve different prop', assert => {
  const msg = 'public: preserves custom property from original';
  const fx = rfx`other`({ bar: 'baz' });
  assert.equal(fx.bar, 'baz', msg);
  assert.end();
});

// Public test: signatures with other non-string values
test('public: rfx signature passes different non-string values', assert => {
  const msg = 'public: handles other types for signature';
  const boolRfx = rfx(true)(function() {});
  assert.equal(boolRfx.rfx.signature, 'true', msg);

  const arrSignature = rfx([1, 2, 3])(function() {});
  assert.equal(arrSignature.rfx.signature, '1,2,3', msg);

  assert.end();
});

// Public test: returned subject mutates with rfx property, other signature
test('public: returned subject is mutated for new sig', assert => {
  const msg = 'public: attaches .rfx to subject, preserves function (new sig)';
  function anotherFn() { return 'ok'; }
  const result = rfx`bar`(anotherFn);

  assert.equal(typeof result.rfx, 'function', msg);
  assert.equal(result.rfx.signature, 'bar', 'correct signature');
  assert.equal(result(), 'ok', 'function call succeeds');
  assert.end();
});

// Public test: check logging to console for a different signature
test('public: rfx.rfx logs alt signature', assert => {
  const fx = rfx`publicsignature`(() => {});
  let captured;
  const oldLog = console.log;
  console.log = function(val) {
    captured = val;
  };
  fx.rfx();
  assert.equal(captured, 'publicsignature', 'logs correct alt signature');
  console.log = oldLog;
  assert.end();
});

// Public test: module.exports.default is rfx (keep logic, diff description)
test('public: module.exports.default identity', assert => {
  const imported = require('../source');
  assert.equal(imported, imported.default, 'default export matches rfx');
  assert.end();
});

// Public test: works as both template literal and regular call, with other string
test('public: both template literal and function string yields same signature', assert => {
  function subject() {}
  const lit = rfx`xyz`(subject);
  const fnc = rfx('xyz')(subject);

  assert.equal(lit.rfx.signature, fnc.rfx.signature, 'public: alt signatures match');
  assert.end();
});