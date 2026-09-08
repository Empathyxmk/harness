// Public test for scss-at-import-partial-extension-disallowed-list with different file extensions
import assert from "assert";

// Simulating: disallowed extensions are ".sass", ".less"
function isPartialExtensionAllowed(importStr) {
  return !(/\.(sass|less)$/.test(importStr));
}

// Valid imports (allowed extensions or none)
assert.ok(isPartialExtensionAllowed("_foo.scss"), "Should allow .scss partials.");
assert.ok(isPartialExtensionAllowed("_bar"), "Should allow no extension partials.");
// Invalid imports (disallowed extensions)
assert.ok(!isPartialExtensionAllowed("_foo.sass"), "Should NOT allow .sass extension.");
assert.ok(!isPartialExtensionAllowed("_bar.less"), "Should NOT allow .less extension.");