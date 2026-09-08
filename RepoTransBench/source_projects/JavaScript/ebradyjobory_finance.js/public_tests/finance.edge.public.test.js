// Public test cases: Same edge/error logic as original, but with different input/output test data

const { expect } = require('chai');
const Finance = require('../finance.js');
const finance = new Finance();

describe('FinanceJS Public Edge Cases & Errors', function () {
  describe('PV', function () {
    it('should handle alternate 0 rate', function () {
      // With 0 rate, PV formula: -cf1 * nper (using different values)
      expect(finance.PV(0, 20, 2, 0)).to.equal(20);
    });

    it('should handle alternate negative cf1', function () {
      // Use different numbers for negative cf1
      // finance.PV(0.07, -200, 5, 0)
      const expected = -200 / Math.pow(1 + 0.07, 5);
      expect(finance.PV(7, -200, 5, 0)).to.be.closeTo(Math.round(expected * 100) / 100, 0.01);
    });

    it('should handle alternate numOfPeriod undefined', function () {
      // Use different values cf1=150, nper=2
      // finance.PV(0.08, 150, 2)
      const expected = 150 / Math.pow(1 + 0.08, 1);
      expect(finance.PV(8, 150, 2)).to.be.closeTo(Math.round(expected * 100) / 100, 0.01);
    });
  });

  describe('FV', function () {
    it('should handle negative rate - new numbers', function () {
      // FV(-0.2, 50, 3, 0)
      const expected = 50 * Math.pow(1 - 0.2, 3);
      expect(finance.FV(-20, 50, 3, 0)).to.be.closeTo(Math.round(expected * 100) / 100, 0.01);
    });
    it('should handle zero period (different cf1)', function () {
      // FV with period 0: -cf1 (choose cf1=250)
      expect(finance.FV(0.05, 250, 0, 0)).to.equal(250);
    });
  });

  describe('NPV', function () {
    it('should handle all zero cash flows (size 5)', function () {
      // NPV(0.1, 0, 0, 0, 0, 0) should be NaN
      expect(finance.NPV(10, 0, 0, 0, 0, 0)).to.satisfy(Number.isNaN);
    });

    it('should handle only initial investment - alternate', function () {
      // NPV(12, -55)
      expect(finance.NPV(12, -55)).to.equal(-55);
    });
  });

  describe('IRR', function () {
    it('should throw if all cash flows positive - alternate', function () {
      expect(() => finance.IRR({cashFlow: [20, 30, 40], depth: 100})).to.throw();
    });

    it('should throw if all cash flows negative - alternate', function () {
      expect(() => finance.IRR({cashFlow: [-15, -25, -35, -45], depth: 100})).to.throw();
    });

    it('should throw if cannot converge - alternate', function () {
      expect(() => finance.IRR({cashFlow: [-75, 0, 0, 0, 0], depth: 10})).to.throw();
    });
  });

  describe('PP', function () {
    it('should handle all negative cash flows, longer period', function () {
      // All negative cash flows (5 of them)
      expect(finance.PP(-20, -30, -20, -25, -10, -5)).to.be.undefined;
    });

    it('should return undefined for uneven cash flows that never recover (different numbers)', function () {
      expect(finance.PP(-200, 15, 17, 15)).to.be.undefined;
    });
  });

  describe('ROI', function () {
    it('should handle zero investment/earnings - different values', function () {
      // (0 - 0) / 0 => NaN
      expect(finance.ROI(0, 0)).to.satisfy(Number.isNaN);
    });

    it('should handle zero earnings (different cost)', function () {
      // (0 - 250) / 250 = -1*100 = -100
      expect(finance.ROI(250, 0)).to.equal(-100);
    });
  });

  describe('AM', function () {
    it('should handle unknown yearOrMonth (edge value)', function () {
      expect(finance.AM(5000, 3, 10, 5)).to.satisfy(Number.isNaN);
    });
  });
});