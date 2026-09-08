const assert = require('assert');
const RandExp = require('../lib/randexp');

describe('RandExp sugar extensions (PUBLIC)', function () {
  it('should allow new RandExp().gen() sugar', function () {
    const re = /foo\d{1,2}/;
    for (let i = 0; i < 10; ++i) {
      const s = new RandExp(re).gen();
      assert(/^foo\d{1,2}$/.test(s), s);
    }
  });

  it('should allow RandExp.call(RegExp)', function () {
    for (let i = 0; i < 7; ++i) {
      const s = RandExp.call(/h[ij]{2}/);
      assert(/^h[ij]{2}$/.test(s));
    }
  });

  it('should support RandExp#toString()', function () {
    const re = /taco\d{0,3}/;
    const r = new RandExp(re);
    assert(typeof r.toString() === 'string');
  });
});