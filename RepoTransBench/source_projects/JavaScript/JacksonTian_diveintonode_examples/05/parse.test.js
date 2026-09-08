function assert(cond, msg) { if (!cond) throw new Error(msg||'assertion failed'); }

console.log("Test: JSON.parse parses valid JSON and throws on invalid JSON");
const jsonStr = '{"a":1}';
let parsed = JSON.parse(jsonStr);
assert(parsed && parsed.a === 1, "Should parse simple JSON");

let invalidThrown = false;
try {
  JSON.parse('{a:1}');
} catch (e) {
  invalidThrown = true;
}
assert(invalidThrown, "Invalid JSON should throw");
console.log("PASS: JSON.parse tests");