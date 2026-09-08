const assert = require('assert');
const RandExp = require('../lib/randexp');

// Test with a much smaller max value than default
describe('RandExp maximum repetitions (PUBLIC)', function () {
  it('should not generate more than custom max repetitions of a character', function () {
    RandExp.prototype.max = 2; // set a small custom max
    const re = /z{2,}/;
    for (let i = 0; i < 10; i++) {
      const res = new RandExp(re).gen();
      assert(
        res.length <= 2 && res.length >= 2,
        `Result length should be between 2 and 2, got ${res.length}`
      );
      assert(/z{2}/.test(res), `Output should conform to /z{2,}/`);
    }
    RandExp.prototype.max = 100; // reset
  });

  it('should apply max for character classes', function () {
    RandExp.prototype.max = 4;
    const re = /[ab]{3,}/;
    for (let i = 0; i < 5; i++) {
      const res = new RandExp(re).gen();
      assert(res.length <= 4 && res.length >= 3);
      assert(/^[ab]+$/.test(res));
    }
    RandExp.prototype.max = 100; // reset
  });
});