// Public test for scss-at-extend-no-missing-placeholder (fixed, new data, correct logic)
import assert from 'assert';

function isPlaceholderExtend(selector) {
  return selector.trim().startsWith('%');
}

// Valid placeholder extend (should return true)
assert.ok(isPlaceholderExtend("%extender"), "Should match extend with placeholder starting with %");
// Invalid (should return false)
assert.ok(!isPlaceholderExtend(".my-class"), "Should NOT match extend without placeholder (no leading %)");