// Public test for color-no-invalid-hex, new invalid and valid hex
import assert from 'assert';

function isValidHex(hex) {
  return /^#[0-9a-f]{3,6}$/i.test(hex);
}

// Different test hex values
assert.ok(isValidHex("#fff"), "Should validate #fff");
assert.ok(isValidHex("#abcdef"), "Should validate #abcdef");
assert.ok(!isValidHex("#abcdz"), "Should invalidate #abcdz");
assert.ok(!isValidHex("#12345g"), "Should invalidate #12345g");