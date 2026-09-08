// Public test for selector-list-comma-newline-after with different selector patterns
import assert from "assert";

// Simulate enforcing comma followed by newline in multi-selector lists
function hasCommaNewlineAfter(str) {
  return /,\n\s*[a-z.#]/.test(str);
}

assert.ok(hasCommaNewlineAfter(".header,\n.footer"), "Valid: comma newline after selector.");
assert.ok(!hasCommaNewlineAfter(".foo, .bar"), "Invalid: no newline after comma.");
assert.ok(hasCommaNewlineAfter("#main,\n  .section"), "Valid: newline and space after comma.");
assert.ok(!hasCommaNewlineAfter("#main, .section"), "Invalid: no newline after comma.");