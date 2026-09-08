// Public test for scss-selector-no-redundant-nesting-selector with varied selectors
import assert from "assert";

// Simulating: selector should not have redundant & (nesting) at beginning
function hasRedundantNesting(selector) {
  // Redundant if selector is `&& .foo`, `& &`
  return /^&\s+&/.test(selector) || selector.includes('&&');
}

assert.ok(!hasRedundantNesting("& .my-class"), "No redundancy: single &.");
assert.ok(!hasRedundantNesting(".foo > &"), "No redundancy when & is after element.");
assert.ok(hasRedundantNesting("&& .bar"), "Redundancy: double & at start.");
assert.ok(hasRedundantNesting("& & .baz"), "Redundancy: spaced double &.");