// Public test for rule-empty-line-before
import assert from 'assert';

function hasEmptyLineBefore(rule) {
  return rule.match(/\n\s*\n[a-zA-Z0-9.#]/) !== null;
}

// Different scenario
assert.ok(hasEmptyLineBefore("\n\n.class { color: blue; }"), "Should have an empty line before rule");
assert.ok(!hasEmptyLineBefore(".btn { color: red; }"), "Should not have empty line before rule");