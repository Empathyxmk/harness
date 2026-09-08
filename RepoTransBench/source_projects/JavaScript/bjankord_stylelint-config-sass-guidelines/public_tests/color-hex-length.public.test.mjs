// Public test for color-hex-length, with different values
import assert from 'assert';

function isLongHex(hex) {
  // Matches 6 digit hex colors (but not 3 digit)
  return /^#[a-f0-9]{6}$/i.test(hex);
}

// Different data: use #123456 (6) and #a1b (3)
assert.ok(isLongHex("#abcdef"), "Should accept 6-digit hex color #abcdef");
assert.ok(!isLongHex("#1a2"), "Should not accept 3-digit hex color #1a2");