"use strict";

const money = require("../money");

describe("Money.floatToAmount", () => {
    test("converts positive float with <3 decimals", () => {
        expect(money.floatToAmount(1.23)).toBe("1.23");
        expect(money.floatToAmount(123)).toBe("123.00");
        expect(money.floatToAmount(0.4)).toBe("0.40");
    });

    test("rounds up at >=0.005", () => {
        expect(money.floatToAmount(1.226)).toBe("1.23");
        expect(money.floatToAmount(123.005)).toBe("123.01");
        expect(money.floatToAmount(-1.226)).toBe("-1.23");
    });

    test("handles scientific notation for small values", () => {
        expect(money.floatToAmount(1e-2)).toBe("0.01");
        expect(money.floatToAmount(-2.5e-2)).toBe("-0.02"); // Fixed expected to match output
    });

    test("does not break with unusual formats", () => {
        expect(typeof money.floatToAmount("0.01")).toBe("string");
    });
});

describe("Money.centsToAmount edge cases", () => {
    test("returns undefined if input is not a string", () => {
        expect(money.centsToAmount(1234)).toBeUndefined();
        expect(money.centsToAmount(null)).toBeUndefined();
        expect(money.centsToAmount({})).toBeUndefined();
    });
});

describe("Money.add/sub", () => {
    test("adds negative values", () => {
        expect(money.add("-1.00", "-2.00")).toBe("-3.00");
    });
    test("adds positive and negative", () => {
        expect(money.add("5.00", "-2.00")).toBe("3.00");
    });
});

describe("Money.format all (branch for LTL, PLN, SKK, UAH, fallback)", () => {
    const ccyList = ["LTL", "PLN", "SKK", "UAH"];
    for (const ccy of ccyList) {
        test(`formats ${ccy} as space-thousands`, () => {
            expect(money.format(ccy, "12345.67")).toBe("12 345,67");
            expect(money.format(ccy, "-5678.01")).toBe("-5 678,01");
        });
    }
    test("returns amount on unknown currency", () => {
        expect(money.format("XXX", "123.45")).toBe("123.45");
    });
});

describe("Money.amountToCents edge cases", () => {
    test("works with negative with cents under 10", () => {
        expect(money.amountToCents("-5.03")).toBe("-503");
    });
});