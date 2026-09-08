// Public test for selector-no-vendor-prefix with new examples
import assert from "assert";

// Simulate detection of vendor prefixes in selectors (e.g., ::-webkit-input-placeholder)
function hasVendorPrefix(selector) {
  return /::-(webkit|moz|ms|o)-/.test(selector);
}

assert.ok(!hasVendorPrefix("::placeholder"), "Allows no vendor prefix");
assert.ok(hasVendorPrefix("::-webkit-scrollbar"), "Disallows webkit vendor prefix");
assert.ok(hasVendorPrefix("::-moz-placeholder"), "Disallows moz vendor prefix");
assert.ok(!hasVendorPrefix(".class"), "Allows class selectors with no vendor prefix");