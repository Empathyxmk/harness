// Public test for declaration-bang-space-after, new scenarios
import assert from 'assert';

function hasSpaceAfterBang(css) {
  return /! [a-zA-Z]+;/.test(css);
}

assert.ok(hasSpaceAfterBang("color: red ! important;"), "Should require space after !");
assert.ok(!hasSpaceAfterBang("color: red !important;"), "Should not allow no space after !");