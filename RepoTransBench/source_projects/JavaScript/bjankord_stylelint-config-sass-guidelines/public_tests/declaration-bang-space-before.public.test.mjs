// Public test for declaration-bang-space-before
import assert from 'assert';

function hasSpaceBeforeBang(css) {
  return /: [a-zA-Z]+ \! important;/.test(css);
}

// New data
assert.ok(hasSpaceBeforeBang("color: green ! important;"), "Should require space before !");
assert.ok(!hasSpaceBeforeBang("color: green! important;"), "Should not allow missing space before !");