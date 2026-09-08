// Public test for string-quotes: enforce single quotes
import assert from "assert";

// Simulate: only valid if single quotes around string
function usesSingleQuotes(value) {
  return /^'[^']*'$/.test(value);
}

assert.ok(usesSingleQuotes("'hello world'"));
assert.ok(usesSingleQuotes("'abc123'"));
assert.ok(!usesSingleQuotes('"double quotes"'));
assert.ok(!usesSingleQuotes("noquotes"));
assert.ok(!usesSingleQuotes("'unmatched"));