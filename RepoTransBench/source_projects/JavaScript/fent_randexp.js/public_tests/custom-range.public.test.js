const assert = require('assert');
const RandExp = require('../lib/randexp');

describe('RandExp custom range (PUBLIC)', function () {
  it('should respect custom range in the pattern', function () {
    const re = /[A-M]{4}/;
    for (let i = 0; i < 5; ++i) {
      const s = new RandExp(re).gen();
      assert(/^[A-M]{4}$/.test(s), `Result "${s}" does not match /^[A-M]{4}$/`);
    }
  });

  it('should handle digit ranges excluding zero', function () {
    const re = /[1-5]{3}/;
    for (let i = 0; i < 5; ++i) {
      const s = new RandExp(re).gen();
      assert(/^[1-5]{3}$/.test(s));
    }
  });

  it('should support unicode range', function () {
    const re = /[\u0400-\u0410]{2}/;
    for (let i = 0; i < 5; ++i) {
      const s = new RandExp(re).gen();
      assert(s.length === 2);
      assert(/^[\u0400-\u0410]{2}$/.test(s), `Got ${s}`);
    }
  });
});