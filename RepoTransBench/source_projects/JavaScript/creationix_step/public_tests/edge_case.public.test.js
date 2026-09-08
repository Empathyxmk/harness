require('./helper');

// Step with no steps (should not throw unless error argument passed)
expect('empty: no error should not throw');
try {
  Step();
  fulfill('empty: no error should not throw');
} catch (e) {
  assert.fail('Should not throw when no steps and no error');
}

// Step with no steps but with error (should throw)
var didThrow = false;
try {
  Step(function() { this('Public error'); });
} catch (e) {
  didThrow = true;
  assert.strictEqual(e, 'Public error');
}
assert.ok(didThrow, 'Should throw error when no steps left and error present in public test');

// Step.fn last arg as function with different number/value
expect('Step.fn last cb public');
var gotCalled = false;
var fn = Step.fn(
  function (val) { this(null, val + 2); }, // +2 instead of +1
  function (err, val) {
    gotCalled = true;
    fulfill('Step.fn last cb public');
    assert.strictEqual(val, 42);
  }
);
fn(40);

// Step.fn with value returned (no custom expectation, just coverage)
var timesTwo = Step.fn(
  function(num) { this(null, num * 2); },
  function(err, val) { return val - 3; }
);
timesTwo(21); // Just covering, different math