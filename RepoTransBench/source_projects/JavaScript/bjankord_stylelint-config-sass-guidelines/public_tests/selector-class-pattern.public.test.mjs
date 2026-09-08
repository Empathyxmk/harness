// Public test for selector-class-pattern
import assert from "assert";

// Simulate: class names should be lowercase, hyphenated, can contain numbers
function isValidClassName(className) {
  return /^[a-z][a-z0-9-]*$/.test(className);
}

assert.ok(isValidClassName("foo-bar1"), "Valid: foo-bar1");
assert.ok(isValidClassName("test42-item"), "Valid: test42-item");
assert.ok(!isValidClassName("FooBar"), "Invalid: capital letters");
assert.ok(!isValidClassName("snake_case"), "Invalid: underscores");
assert.ok(!isValidClassName("42start"), "Invalid: cannot start with number");
assert.ok(!isValidClassName("-prefixed"), "Invalid: cannot start with hyphen");