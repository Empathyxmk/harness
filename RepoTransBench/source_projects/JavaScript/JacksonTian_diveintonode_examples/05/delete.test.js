function assert(cond, msg) { if (!cond) throw new Error(msg||'assertion failed'); }

console.log("Test: deleting non-existing property does not throw");
const obj = { a: 1 };
try {
  delete obj.b;
  console.log("PASS: delete obj.b did not throw");
} catch (e) {
  console.error("FAIL:", e);
  process.exit(1);
}
assert(!('b' in obj), "Property b should not exist in obj");