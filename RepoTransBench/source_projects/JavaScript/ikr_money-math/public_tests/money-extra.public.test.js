const money = require('../money');

describe("Money.floatToAmount - public cases", () => {
    test("rounds up at >=0.005 - public data", () => {
        expect(money.floatToAmount(12.345)).toBe("12.35");
        expect(money.floatToAmount(7.996)).toBe("8.00");
        expect(money.floatToAmount(7.935)).toBe("7.94");
        expect(money.floatToAmount(-2.574)).toBe("-2.57");
    });

    test("handles scientific notation for small values - new data", () => {
        expect(money.floatToAmount(5e-5)).toBe("0.00");
        expect(money.floatToAmount(3.455e-1)).toBe("0.35");
    });
});

describe("Money internal - public additional", () => {
    test("handles string values as input - public data", () => {
        expect(money.floatToAmount("17.888")).toBe("17.89");
        expect(money.floatToAmount("-42.0587")).toBe("-42.06");
    });
});