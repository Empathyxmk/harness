// Public test for function-comma-space-after
import assert from 'assert';

function hasSpaceAfterComma(val) {
  return /,\s/.test(val);
}

// Different data
assert.ok(hasSpaceAfterComma("rgba(0, 255, 0, 0.7)"), "Should have space after comma");
assert.ok(!hasSpaceAfterComma("rgba(0,255,0,0.7)"), "Should not have space after comma");