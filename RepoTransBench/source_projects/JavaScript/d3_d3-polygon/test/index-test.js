import * as d3Polygon from "../src/index.js";

it("d3Polygon exports all main polygon methods", () => {
  [
    "polygonArea",
    "polygonCentroid",
    "polygonContains",
    "polygonHull",
    "polygonLength"
  ].forEach(key => {
    if (typeof d3Polygon[key] !== "function") throw new Error(`${key} not exported as a function`);
  });
});