// Public test for selector-pseudo-element-colon-notation: require double colon for all pseudo-elements
import assert from "assert";

// Simulate: only double colon (::) notation allowed
function usesDoubleColon(selector) {
  // Accepts .foo::after but not .foo:after
  return !(/:[a-z]/.test(selector) && !/::[a-z]/.test(selector));
}

assert.ok(usesDoubleColon(".b::before"), "Valid: double colon notation");
assert.ok(usesDoubleColon(".c::after"), "Valid: double colon notation");
assert.ok(!usesDoubleColon(".foo:before"), "Invalid: single colon used");
assert.ok(!usesDoubleColon(".bar:after"), "Invalid: single colon used");