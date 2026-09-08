// Minimalist runner for non-Jest environments
function assert(cond, msg) { if (!cond) throw new Error(msg||'assertion failed'); }

console.log("Test: 02/extensions.js can be required without error");
try {
  require('./extensions.js');
  console.log("PASS: require('./extensions.js') did not throw");
} catch (e) {
  console.error("FAIL:", e);
  process.exit(1);
}

assert(typeof require.extensions['.js'] === "function", ".js extension should be registered");
assert(typeof require.extensions['.json'] === "function", ".json extension should be registered");
assert(typeof require.extensions['.node'] === "function", ".node extension should be registered");
console.log("PASS: extensions registered");