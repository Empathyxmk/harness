// Converted for Jest from Mocha
"use strict";

const money = require("../money");
const assert = require("assert");

describe("money.amountToCents()", function () {
    test("works on positive amount", function () {
        expect(money.amountToCents("126.99")).toBe("12699");
    });

    test("works on negative amount", function () {
        expect(money.amountToCents("-10001.00")).toBe("-1000100");
    });

    test("works on just cents, removes 0 from start", function () {
        expect(money.amountToCents("0.99")).toBe("99");
    });
});

describe("money.centsToAmount()", function () {
    test("works on positive amount", function () {
        expect(money.centsToAmount("2000010")).toBe("20000.10");
    });

    test("works on negative amount", function () {
        expect(money.centsToAmount("-1000100")).toBe("-10001.00");
    });

    test("works on a negative fraction", function () {
        expect(money.centsToAmount("-32")).toBe("-0.32");
    });

    test("works on a tiny negative fraction", function () {
        expect(money.centsToAmount("-1")).toBe("-0.01");
    });

    test("works for zero", function () {
        expect(money.centsToAmount("0")).toBe("0.00");
    });

    test("works for one", function () {
        expect(money.centsToAmount("1")).toBe("0.01");
    });

    test("works for ten", function () {
        expect(money.centsToAmount("10")).toBe("0.10");
    });

    test("is undefined on undefined", function () {
        expect(money.centsToAmount()).toBeUndefined();
    });
});

describe("money.integralPart", function () {
    test("returns the value before the decimal separator for a positive amount", function () {
        expect(money.integralPart("12.00")).toBe("12");
    });

    test("returns the value before the decimal separator for a negative amount", function () {
        expect(money.integralPart("-55.10")).toBe("-55");
    });

    test("returns zero for zero", function () {
        expect(money.integralPart("0.00")).toBe("0");
    });
});

describe("money.format()", function () {
    test("works for CHF", function () {
        expect(money.format("CHF", "560.05")).toBe("560.05");
        expect(money.format("CHF", "-1560.00")).toBe("-1,560.00");
    });

    test("works for JPY", function () {
        expect(money.format("JPY", "560.00")).toBe("560");
        expect(money.format("JPY", "236800.00")).toBe("236,800");
        expect(money.format("JPY", "-1000000000.00")).toBe("-1,000,000,000");
        expect(money.format("JPY", "-100000000000.00")).toBe("-100,000,000,000");
    });

    test("works for EUR", function () {
        expect(money.format("EUR", "560.00")).toBe("560,00");
        expect(money.format("EUR", "-1560.00")).toBe("-1.560,00");
        expect(money.format("EUR", "-100000000000.00")).toBe("-100.000.000.000,00");
    });

    test("works for SEK", function () {
        expect(money.format("SEK", "560.00")).toBe("560,00");
        expect(money.format("SEK", "-1560.00")).toBe("-1 560,00");
        expect(money.format("SEK", "-100000000000.00")).toBe("-100 000 000 000,00");
    });
});

describe("money.add()", function () {
    test("sums positive decimals 1", function () {
        expect(money.add("16.11", "17.07")).toBe("33.18");
    });

    test("sums positive decimals 2", function () {
        expect(money.add("65535.79", "1024.85")).toBe("66560.64");
    });

    test("sums positive decimals 3", function () {
        expect(money.add("1.99", "0.02")).toBe("2.01");
    });

    test("sums positive decimals 4", function () {
        expect(money.add("1.90", "0.10")).toBe("2.00");
    });
});