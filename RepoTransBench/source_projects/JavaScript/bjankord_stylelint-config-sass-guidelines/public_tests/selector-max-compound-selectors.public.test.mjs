// Public test for selector-max-compound-selectors
import assert from "assert";

// Simulate: max compound selectors per selector (3)
function isValidCompoundCount(selector, max = 3) {
  // Split by combinators and count compounds
  return selector.trim().split(/\s+/).length <= max;
}

assert.ok(isValidCompoundCount("a b c"), "Valid: exactly at max");
assert.ok(isValidCompoundCount(".foo .bar .baz"), "Valid: 3 compounds, at max");
assert.ok(!isValidCompoundCount("section a.foo .bar .baz"), "Invalid: 4 compounds");
assert.ok(!isValidCompoundCount("div span strong em"), "Invalid: 4 compounds");
assert.ok(isValidCompoundCount(".test"), "Valid: only one compound");