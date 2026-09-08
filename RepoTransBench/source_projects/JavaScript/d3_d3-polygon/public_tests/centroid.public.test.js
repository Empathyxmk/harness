import assert from "assert";
import {polygonCentroid} from "../src/index.js";

// Closed counterclockwise polygon (rectangle at [2,2], [2,4], [6,4], [6,2])
it("polygonCentroid(points) returns the expected value for a different closed counterclockwise polygon", () => {
  assert.deepStrictEqual(polygonCentroid([[2, 2], [2, 4], [6, 4], [6, 2], [2, 2]]), [4, 3]);
});

// Closed clockwise polygon (triangle with non-standard points)
it("polygonCentroid(points) returns the expected value for a different closed clockwise polygon", () => {
  assert.deepStrictEqual(polygonCentroid([[2, 4], [4, 7], [7, 2], [2, 4]]), [4.333333333333333, 4.333333333333333]);
});

// Open counterclockwise polygon (pentagon, non-regular)
it("polygonCentroid(points) returns the expected value for a different open counterclockwise polygon", () => {
  assert.deepStrictEqual(
    polygonCentroid([
      [0, 0],
      [1, 3],
      [4, 4],
      [6, 1],
      [3, -2]
    ]),
    [2.6027397260273974, 1.0289855072463768]
  );
});

// Open clockwise polygon (different diamond shape)
it("polygonCentroid(points) returns the expected value for a different open clockwise polygon", () => {
  assert.deepStrictEqual(
    polygonCentroid([
      [4, 0],
      [8, 4],
      [4, 8],
      [0, 4]
    ]),
    [4, 4]
  );
});

// Large polygon test with different parameters
it("polygonCentroid(polygon) returns the expected value for a different very large polygon", () => {
  const stop = 5e7;
  const step = 5e3;
  const points = [];
  for (let value = 0; value < stop; value += step) points.push([2, value]);
  for (let value = 0; value < stop; value += step) points.push([value+2, stop]);
  for (let value = stop - step; value >= 0; value -= step) points.push([stop+2, value]);
  for (let value = stop - step; value >= 0; value -= step) points.push([value+2, 0]);
  // For this rectangle shape, centroid will be at ([stop/2 + 2], stop/2)
  assert.deepStrictEqual(
    polygonCentroid(points),
    [stop / 2 + 2, stop / 2]
  );
});