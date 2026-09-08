// Public test for selector-no-qualifying-type with new scenarios
import assert from "assert";

/*
  Simulate: Disallow qualifying types (e.g., input.button, a.link)
  Allow: only class or id selectors
*/
function isQualifyingType(selector) {
  return /\b[a-zA-Z][a-zA-Z0-9-]*[.#][a-zA-Z0-9_-]/.test(selector);
}

assert.ok(!isQualifyingType(".foo-bar"), "Allows class without type");
assert.ok(!isQualifyingType("#main-section"), "Allows id without type");
assert.ok(isQualifyingType("ul.menu"), "Disallow element with class");
assert.ok(isQualifyingType("span#error"), "Disallow element with id");
assert.ok(!isQualifyingType("[type=\"text\"]"), "Allows attribute selector only");