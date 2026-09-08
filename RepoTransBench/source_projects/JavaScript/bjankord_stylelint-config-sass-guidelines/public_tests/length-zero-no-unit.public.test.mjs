// Public test for length-zero-no-unit
import assert from 'assert';

const cssWithUnit = "margin: 0px;";
const cssWithoutUnit = "padding: 0;";

assert.ok(/0px/.test(cssWithUnit), "Length zero with unit, should be flagged by linter");
assert.ok(/0;/.test(cssWithoutUnit), "Length zero without unit, which is preferred");