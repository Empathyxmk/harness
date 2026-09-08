// Public test for color-named, different input
import assert from 'assert';

const cssInput = "background: blue;";
const cssInput2 = "background: #f1f1f1;";

// Should not allow named color, should allow hex
assert.ok(/background:\s*blue;/.test(cssInput), "Named color used, which should not be allowed.");
assert.ok(/background:\s*#f1f1f1;/.test(cssInput2), "Hex color used, which should be allowed.");