// Public test for scss-at-function-pattern with different test data
import assert from "assert";

// Simulate a function name validation pattern rule
// Example config: /^myFunc_.*/
function matchesFunctionPattern(name) {
  return /^custom_[a-z_]+$/.test(name);
}

// Valid names
assert.ok(matchesFunctionPattern('custom_calc_width'), "Should match custom_ function name.");
assert.ok(matchesFunctionPattern('custom_process_value'), "Should match custom_ function name.");
// Invalid names (should NOT match)
assert.ok(!matchesFunctionPattern('notcustom_width'), "Should not match function name without custom_.");
assert.ok(!matchesFunctionPattern('_custom_wrong'), "Should not match function name that starts with underscore.");