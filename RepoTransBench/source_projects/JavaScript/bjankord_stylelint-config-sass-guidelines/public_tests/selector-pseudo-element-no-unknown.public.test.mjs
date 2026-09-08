// Public test for selector-pseudo-element-no-unknown with custom pseudo-elements
import assert from "assert";

// Simulate: only known pseudo-elements allowed
const known = [ "before", "after", "first-letter", "first-line", "backdrop" ];

function isKnownPseudoElement(name) {
  return known.includes(name.replace(/^:+/, ""));
}

assert.ok(isKnownPseudoElement("::before"), "Known pseudo-element: before");
assert.ok(isKnownPseudoElement("::backdrop"), "Known pseudo-element: backdrop");
assert.ok(!isKnownPseudoElement("::customfoo"), "Unknown pseudo-element: customfoo");
assert.ok(!isKnownPseudoElement("::magicline"), "Unknown pseudo-element: magicline");