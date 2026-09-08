import assert from "assert";
import cross from "../src/cross.js";

// A simple right triangle at origin, counter-clockwise: expect >0
it("cross(a, b, c) returns positive for counterclockwise", () => {
  assert(cross([0, 0], [1, 0], [0, 1]) > 0);
});

// Clockwise triangle: expect <0
it("cross(a, b, c) returns negative for clockwise", () => {
  assert(cross([0, 0], [0, 1], [1, 0]) < 0);
});

// Collinear points: expect 0
it("cross(a, b, c) returns 0 for collinear points", () => {
  assert.strictEqual(cross([0, 0], [1, 1], [2, 2]), 0);
});

// All points equal: degenerate case, expect 0
it("cross(a, b, c) returns 0 for same points", () => {
  assert.strictEqual(cross([1, 1], [1, 1], [1, 1]), 0);
});

// Negative coordinates
it("cross(a, b, c) correctly handles negative coordinates", () => {
  assert.strictEqual(cross([-1, 0], [0, -1], [1, 0]), 2);
});