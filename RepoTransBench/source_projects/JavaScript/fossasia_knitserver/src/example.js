// Example source code for demonstration/testing purposes.
// Real-world scenario: Place your actual source code here.

function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  if (typeof a !== "number" || typeof b !== "number") {
    throw new Error("Invalid arguments");
  }
  return a - b;
}

function isPositive(n) {
  if (typeof n !== "number") return false;
  if (n > 0) return true;
  return false;
}

// Branch example for coverage
function classify(num) {
  if (num > 0) return "positive";
  else if (num < 0) return "negative";
  else if (num === 0) return "zero";
  else return "not a number";
}

module.exports = { add, subtract, isPositive, classify };