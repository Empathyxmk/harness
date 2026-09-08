const { add, max, isEven, greet } = require("./utils");

describe("add", () => {
    test("adds positives", () => {
        expect(add(2, 3)).toBe(5);
    });
    test("adds negatives", () => {
        expect(add(-2, -5)).toBe(-7);
    });
});

describe("max", () => {
    test("returns first if greater", () => {
        expect(max(10, 2)).toBe(10);
    });
    test("returns second if greater", () => {
        expect(max(3, 9)).toBe(9);
    });
    test("returns either if equal", () => {
        expect([7, 7]).toContain(max(7, 7));
    });
});

describe("isEven", () => {
    test("true for even numbers", () => {
        expect(isEven(4)).toBe(true);
    });
    test("false for odd numbers", () => {
        expect(isEven(7)).toBe(false);
    });
    test("throws for non-number", () => {
        expect(() => isEven("str")).toThrow("Input must be a number");
    });
});

describe("greet", () => {
    test("greets by name", () => {
        expect(greet("Dmitry")).toBe("Hello, Dmitry!");
    });
    test("greets world if no name", () => {
        expect(greet()).toBe("Hello, world!");
    });
    test("greets world for falsy name", () => {
        expect(greet("")).toBe("Hello, world!");
    });
});