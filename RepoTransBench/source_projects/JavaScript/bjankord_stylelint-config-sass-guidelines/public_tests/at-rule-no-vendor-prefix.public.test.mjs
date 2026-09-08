// Public test for at-rule-no-vendor-prefix
import assert from 'assert';

const css1 = "@-webkit-keyframes fadeIn {}";
const css2 = "@keyframes fadeIn {}";

// Different data: test for presence of vendor prefix
assert.ok(/^@-webkit-/.test(css1), "Should detect vendor-prefixed at-rule");
assert.ok(!/^@-webkit-/.test(css2), "Should not detect vendor-prefixed at-rule on standard at-rule");