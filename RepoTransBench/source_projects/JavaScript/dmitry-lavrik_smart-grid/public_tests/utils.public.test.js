const { add, max, isEven, greet } = require("../src/utils");

describe("add", () => {
    test("adds positives", () => {
        expect(add(4, 7)).toBe(11);
    });
    test("adds negatives", () => {
        expect(add(-6, -1)).toBe(-7);
    });
});

describe("max", () => {
    test("returns first if greater", () => {
        expect(max(15, 4)).toBe(15);
    });
    test("returns second if greater", () => {
        expect(max(5, 12)).toBe(12);
    });
    test("returns either if equal", () => {
        expect([20, 20]).toContain(max(20, 20));
    });
});

describe("isEven", () => {
    test("true for even numbers", () => {
        expect(isEven(10)).toBe(true);
    });
    test("false for odd numbers", () => {
        expect(isEven(11)).toBe(false);
    });
    test("throws for non-number", () => {
        expect(() => isEven(null)).toThrow("Input must be a number");
    });
});

describe("greet", () => {
    test("greets by name", () => {
        expect(greet("Alex")).toBe("Hello, Alex!");
    });
    test("greets world if no name", () => {
        expect(greet(undefined)).toBe("Hello, world!");
    });
    test("greets world for falsy name", () => {
        expect(greet(0)).toBe("Hello, world!");
    });
});