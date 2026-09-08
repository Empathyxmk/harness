"use strict";

const money = require("../money");
const assert = require("assert");

describe("money.amountToCents() - public cases", function () {
    test("works on positive amount (different amount)", function () {
        expect(money.amountToCents("305.25")).toBe("30525");
    });

    test("works on negative amount (different amount)", function () {
        expect(money.amountToCents("-12.34")).toBe("-1234");
    });

    test("works on just cents but different than .99", function () {
        expect(money.amountToCents("0.01")).toBe("1");
    });
});

describe("money.centsToAmount() - public cases", function () {
    test("works on positive amount (different value)", function () {
        expect(money.centsToAmount("507")).toBe("5.07");
    });

    test("works on negative amount (different value)", function () {
        expect(money.centsToAmount("-20300")).toBe("-203.00");
    });

    test("works on a negative fraction (different value)", function () {
        expect(money.centsToAmount("-56")).toBe("-0.56");
    });

    test("works on a tiny negative fraction (smaller)", function () {
        expect(money.centsToAmount("-6")).toBe("-0.06");
    });

    test("works for zero (same logic)", function () {
        expect(money.centsToAmount("0")).toBe("0.00");
    });

    test("works for a small positive", function () {
        expect(money.centsToAmount("7")).toBe("0.07");
    });

    test("works for a double digit", function () {
        expect(money.centsToAmount("80")).toBe("0.80");
    });

    test("is undefined on undefined", function () {
        expect(money.centsToAmount()).toBeUndefined();
    });
});

describe("money.integralPart - public cases", function () {
    test("positive different amount", function () {
        expect(money.integralPart("853.20")).toBe("853");
    });

    test("negative different amount", function () {
        expect(money.integralPart("-75.15")).toBe("-75");
    });

    test("returns zero for zero (same logic)", function () {
        expect(money.integralPart("0.00")).toBe("0");
    });
});

describe("money.format() - public cases", function () {
    test("works for CHF - different values", function () {
        expect(money.format("CHF", "1000.01")).toBe("1,000.01");
        expect(money.format("CHF", "-2589.50")).toBe("-2,589.50");
    });

    test("works for JPY - different values", function () {
        expect(money.format("JPY", "870.00")).toBe("870");
        expect(money.format("JPY", "4625800.00")).toBe("4,625,800");
        expect(money.format("JPY", "-2500.00")).toBe("-2,500");
        expect(money.format("JPY", "-800000000.00")).toBe("-800,000,000");
    });

    test("works for EUR - different values", function () {
        expect(money.format("EUR", "311.00")).toBe("311,00");
        expect(money.format("EUR", "-412.00")).toBe("-412,00");
        expect(money.format("EUR", "-1501.10")).toBe("-1.501,10");
    });

    test("works for SEK - different values", function () {
        expect(money.format("SEK", "71.25")).toBe("71,25");
        expect(money.format("SEK", "-3339.00")).toBe("-3 339,00");
        expect(money.format("SEK", "-55555.55")).toBe("-55 555,55");
    });
});

describe("money.add() - public cases", function () {
    test("sums positive decimals with unique values", function () {
        expect(money.add("20.15", "30.08")).toBe("50.23");
        expect(money.add("1234.56", "789.01")).toBe("2023.57");
        expect(money.add("4.44", "5.55")).toBe("9.99");
        expect(money.add("99.50", "0.50")).toBe("100.00");
    });
});