// Sample JavaScript module added to enable test generation and coverage demonstration.
// Replace this with your actual project source files as needed.

function add(a, b) {
  return a + b;
}

function max(arr) {
  if (!arr || arr.length === 0) return null;
  let m = arr[0];
  for (let i = 1; i < arr.length; i++) {
    if (arr[i] > m) {
      m = arr[i];
    }
  }
  return m;
}

module.exports = {
  add,
  max
};