const assert = require('assert');
const RandExp = require('../lib/randexp');

// Custom PRNG that always returns 0
const zeroPrng = () => 0;

describe('RandExp custom PRNG/seed (PUBLIC)', function () {
  it('should use custom PRNG that always returns minimum value', function () {
    const randexp = new RandExp(/[cde]{2}/);
    randexp.randInt = (a, b) => a; // always minimum
    const out = randexp.gen();
    assert(
      /^[cde]{2}$/.test(out),
      `Output "${out}" does not match pattern`
    );
  });

  it('should produce predictable output for a numeric PRNG', function () {
    let state = 7;
    const prng = () => {
      state = (state * 5 + 3) % 13;
      return state / 13;
    };
    const randexp = new RandExp(/[klm]{3}/);
    randexp.randInt = (a, b) => a + Math.floor(prng() * (b - a + 1));
    const out = randexp.gen();
    assert(/^[klm]{3}$/.test(out));
  });
});