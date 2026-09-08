require('./helper');

// Test: Step with no steps (should not throw unless error argument passed)
expect('noStep: no error should not throw');
try {
  Step();
  fulfill('noStep: no error should not throw');
} catch (e) {
  assert.fail('Should not throw when no steps and no error');
}

// Test: Step with no steps but with error (should throw)
var threw = false;
try {
  Step(function() { this('Test error'); });
} catch (e) {
  threw = true;
  assert.strictEqual(e, 'Test error');
}
assert.ok(threw, 'Should throw error when no steps left and error present');

// Test: Step.fn last arg as function
expect('Step.fn custom last callback');
var called = false;
var fn = Step.fn(
  function (val) { this(null, val + 1); },
  function (err, val) {
    called = true;
    fulfill('Step.fn custom last callback');
    assert.strictEqual(val, 6);
  }
);
fn(5);

// Test: Step.fn with value returned (no custom expectation, just exercise coverage)
var addOne = Step.fn(
  function(num) { this(null, num + 1); },
  function(err, val) { return val * 2; }
);
addOne(10); // Not asserting return, just covering internal branch

// Also test synchronous returns from step function
expect('Synchronous return in step');
var sync = false;
Step(
  function () {
    sync = true;
    return 123;
  },
  function (err, val) {
    fulfill('Synchronous return in step');
    assert.strictEqual(val, 123);
  }
);
assert.ok(sync, 'First step was run synchronously');