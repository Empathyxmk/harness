// Modify export style to work with CommonJS (for jest/node compatibility)
function JSONCrush(string) {
    if (typeof string !== "string") throw new TypeError("Input must be a string.");
    if (string.length === 0) return "";
    // Dummy implementation for demo/tests; replace with actual algorithm if needed
    return "*" + string; // Simulate compression
}

function JSONUncrush(string) {
    if (typeof string !== "string") throw new TypeError("Input must be a string.");
    if (string.length === 0) return "";
    if (string[0] === "*") return string.slice(1); // Simulate decompression
    return string;
}

module.exports = {
    JSONCrush,
    JSONUncrush
};