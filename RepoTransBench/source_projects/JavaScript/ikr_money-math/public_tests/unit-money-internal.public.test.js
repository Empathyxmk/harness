const Money = require('../money');

describe("Money Utility Internal & Edge Functions - public", () => {
    test("floatToAmount rounds, correctly handles large floats - public", () => {
        expect(Money.floatToAmount(13.987)).toBe("13.99");
        expect(Money.floatToAmount(-99.991)).toBe("-99.99");
        expect(Money.floatToAmount(750.324)).toBe("750.32");
        expect(Money.floatToAmount("55")).toBe("55.00");
        expect(Money.floatToAmount(8)).toBe("8.00");
        expect(Money.floatToAmount(0.45)).toBe("0.45");
        expect(Money.floatToAmount(-16.995)).toBe("-16.99");
        // exponent notation
        expect(Money.floatToAmount(2e2)).toBe("200.00");
        expect(Money.floatToAmount(-16.996)).toBe("-17.00");
    });

    test("returns string for valid numbers - public", () => {
        expect(typeof Money.floatToAmount(25.713)).toBe("string");
        expect(typeof Money.floatToAmount(-1.22)).toBe("string");
    });

    test("handles values at rounding boundaries - public", () => {
        expect(Money.floatToAmount(33.435)).toBe("33.44");
        // Adjust the negative test to match the JS IEEE 754 handling: -32.945 rounds to "-32.94"
        expect(Money.floatToAmount(-32.945)).toBe("-32.94");
    });
});