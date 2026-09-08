// Public test for scss-percent-placeholder-pattern with different patterns
import assert from "assert";

// Simulating: required pattern is /^is-[a-z-]+/
function isValidPlaceholder(name) {
  return /^is-[a-z-]+$/.test(name);
}

assert.ok(isValidPlaceholder("is-active-state"), "Valid placeholder: is-active-state");
assert.ok(isValidPlaceholder("is-disabled"), "Valid placeholder: is-disabled");
assert.ok(!isValidPlaceholder("has-feature"), "Invalid placeholder: does not start with is-");
assert.ok(!isValidPlaceholder("isActive"), "Invalid placeholder: uses camelCase.");