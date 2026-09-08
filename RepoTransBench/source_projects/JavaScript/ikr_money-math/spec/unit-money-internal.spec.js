// Enhanced coverage of money.js: test edge and uncovered cases, especially on internal/util methods

const path = require("path");
const { BigInteger } = require("jsbn");
const moneyModule = require("../money.js");
const Money = moneyModule;

describe("Money Utility Internal & Edge Functions", () => {
  // For coverage: Currency.prototype.format (default)
  it("should return amount for unknown currency code (Currency.prototype.format)", () => {
    expect(Money.format("XXX", "1234567.89")).toBe("1234567.89");
  });

  // Money.amountToCents
  it("amountToCents strips dot and leading zeros", () => {
    expect(Money.amountToCents("00123.45")).toBe("12345");
    expect(Money.amountToCents("0.01")).toBe("1");
    expect(Money.amountToCents("123.45")).toBe("12345");
    // according to impl: "000.00" -> "" ("" is correct as no nonzero digits remain)
    expect(Money.amountToCents("000.00")).toBe(""); 
  });

  it("centsToAmount returns undefined for non-string input", () => {
    expect(Money.centsToAmount(123)).toBeUndefined();
    expect(Money.centsToAmount(null)).toBeUndefined();
    expect(Money.centsToAmount(undefined)).toBeUndefined();
    expect(Money.centsToAmount({})).toBeUndefined();
  });

  it("centsToAmount handles negative and small values", () => {
    expect(Money.centsToAmount("-1")).toBe("-0.01");
    expect(Money.centsToAmount("-12")).toBe("-0.12");
    expect(Money.centsToAmount("-123")).toBe("-1.23");
    expect(Money.centsToAmount("1")).toBe("0.01");
    expect(Money.centsToAmount("12")).toBe("0.12");
    expect(Money.centsToAmount("123456")).toBe("1234.56");
  });

  it("floatToAmount rounds, correctly handles large floats", () => {
    expect(Money.floatToAmount(1.005)).toBe("1.01"); // rounds up
    expect(Money.floatToAmount(1.004)).toBe("1.00"); // does not round
    expect(Money.floatToAmount(3)).toBe("3.00");
    expect(Money.floatToAmount(0.1)).toBe("0.10");
    expect(Money.floatToAmount(-1.999)).toBe("-2.00");
    // exponent notation
    expect(Money.floatToAmount(1e2)).toBe("100.00");
    // covers isNegative suffix rounding branch
    expect(Money.floatToAmount(-1.996)).toBe("-2.00");
  });

  it("integralPart returns the integer (no decimals)", () => {
    expect(Money.integralPart("123.45")).toBe("123");
    expect(Money.integralPart("-99.10")).toBe("-99");
  });

  it("format dispatches to Currency formatter", () => {
    expect(Money.format("USD", "12345.67")).toBe("12,345.67");
    expect(Money.format("EUR", "12345.67")).toBe("12.345,67");
    expect(Money.format("SEK", "12345.67")).toBe("12 345,67");
    expect(Money.format("JPY", "12345.67")).toBe("12,345");
    expect(Money.format("GBP", "12345.67")).toBe("12.345,67");
    expect(Money.format("CHF", "12345.67")).toBe("12,345.67");
    expect(Money.format("LTL", "12345.67")).toBe("12 345,67");
    expect(Money.format("PLN", "12345.67")).toBe("12 345,67");
    expect(Money.format("SKK", "12345.67")).toBe("12 345,67");
    expect(Money.format("UAH", "12345.67")).toBe("12 345,67");
  });

  it("add/subtract/mul/div basic properties", () => {
    expect(Money.add("1.00", "1.00")).toBe("2.00");
    expect(Money.subtract("2.00", "0.50")).toBe("1.50");
    expect(Money.mul("2.00", "3.00")).toBe("6.00");
    expect(Money.mul("2.25", "2.00")).toBe("4.50");
    expect(Money.div("6.00", "2.00")).toBe("3.00");
    expect(Money.div("7.00", "2.00")).toBe("3.50");
    expect(Money.div("1.00", "3.00")).toBe("0.33");
    expect(Money.mul("999.99", "0.01")).toBe("10.00");
  });

  it("percent: handles >0.5 rounding and edge mods", () => {
    expect(Money.percent("100.00", "50.00")).toBe("50.00");
    expect(Money.percent("100.00", "23.45")).toBe("23.45");
    expect(Money.percent("1.00", "99.99")).toBe("1.00");
    expect(Money.percent("1.00", "99.98")).toBe("1.00");
  });

  it("roundUpTo5Cents covers lastDigit logic", () => {
    expect(Money.roundUpTo5Cents("1.01")).toBe("1.05");
    expect(Money.roundUpTo5Cents("1.02")).toBe("1.05");
    expect(Money.roundUpTo5Cents("1.03")).toBe("1.05");
    expect(Money.roundUpTo5Cents("1.04")).toBe("1.05");
    expect(Money.roundUpTo5Cents("1.05")).toBe("1.05"); // already 5-mult

    expect(Money.roundUpTo5Cents("21.10")).toBe("21.10");
    expect(Money.roundUpTo5Cents("21.13")).toBe("21.15");
    expect(Money.roundUpTo5Cents("21.17")).toBe("21.20");
  });

  it("roundTo5Cents rounds values (calls mul/div/round)", () => {
    // roundTo5Cents can round up if close to .05 chunk
    expect(Money.roundTo5Cents("1.03")).toBe("1.05");
    expect(Money.roundTo5Cents("1.02")).toBe("1.00");
    expect(Money.roundTo5Cents("2.08")).toBe("2.10");
    expect(Money.roundTo5Cents("2.04")).toBe("2.05"); // IMP: It's "2.05" by code's actual rounding behavior
  });

  it("cmp, isEqual, isZero, isNegative, isPositive cases", () => {
    expect(Money.cmp("3.00", "2.00")).toBeGreaterThan(0);
    expect(Money.cmp("2.00", "2.00")).toBe(0);
    expect(Money.cmp("1.00", "2.00")).toBeLessThan(0);

    expect(Money.isEqual("2.00", "2.00")).toBe(true);
    expect(Money.isZero("0.00")).toBe(true);
    expect(Money.isZero("0.01")).toBe(false);
    expect(Money.isNegative("-1.00")).toBe(true);
    expect(Money.isNegative("0.00")).toBe(false);
    expect(Money.isPositive("2.00")).toBe(true);
    expect(Money.isPositive("-2.00")).toBe(false);
  });

  it("isGreaterThan, isGreaterOrEqualTo/isLessThan/isLessOrEqualTo", () => {
    expect(Money.isGreaterThan("2.00", "1.00")).toBe(true);
    expect(Money.isGreaterOrEqualTo("2.00", "2.00")).toBe(true);
    expect(Money.isGreaterOrEqualTo("3.00", "2.00")).toBe(true);
    expect(Money.isLessThan("2.00", "3.00")).toBe(true);
    expect(Money.isLessThan("3.00", "3.00")).toBe(false);
    expect(Money.isLessOrEqualTo("3.00", "3.00")).toBe(true);
    expect(Money.isLessOrEqualTo("2.00", "3.00")).toBe(true);
  });
});