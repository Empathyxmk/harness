// Public test for selector-max-id with different selectors and allowed max id = 2
import assert from "assert";

// Simulate counting # occurrences (ids)
function isValidIdCount(selector, maxIds = 2) {
  return (selector.match(/#/g) || []).length <= maxIds;
}

// Valid: 2 or fewer IDs
assert.ok(isValidIdCount("#foo"), "Allows 1 id selector");
assert.ok(isValidIdCount("#foo #bar"), "Allows 2 id selectors");

// Invalid: More than 2 IDs
assert.ok(!isValidIdCount("#a #b #c"), "Disallows 3 id selectors");
assert.ok(!isValidIdCount("#id1 #id2 #id3 .test"), "Disallows 3 ids and a class");