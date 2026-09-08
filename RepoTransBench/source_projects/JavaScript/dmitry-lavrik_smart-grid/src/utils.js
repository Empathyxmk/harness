// Example utility functions for coverage and testing demonstration

function add(a, b) {
    return a + b;
}

function max(a, b) {
    return a > b ? a : b;
}

function isEven(n) {
    if (typeof n !== "number") {
        throw new Error("Input must be a number");
    }
    return n % 2 === 0;
}

function greet(name) {
    if (!name) {
        return "Hello, world!";
    }
    return `Hello, ${name}!`;
}

module.exports = { add, max, isEven, greet };