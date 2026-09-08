const assert = require('assert');
const RandExp = require('../lib/randexp');

// More comprehensive visible (public) tests
describe('RandExp - general coverage (PUBLIC)', function () {
  it('should generate valid emails', function () {
    const re = /\w{4,9}@test\.org/;
    for (let i = 0; i < 10; i++) {
      const s = new RandExp(re).gen();
      assert(/^[A-Za-z0-9_]{4,9}@test\.org$/.test(s));
    }
  });

  it('should handle groups and quantifiers', function () {
    const re = /(hi|bye){3}/;
    for (let i = 0; i < 5; i++) {
      const s = new RandExp(re).gen();
      assert(/^(hi|bye){3}$/.test(s));
    }
  });

  it('should handle optional groups', function () {
    const re = /^ok(yes)?$/;
    for (let i = 0; i < 8; i++) {
      const s = new RandExp(re).gen();
      assert(/^ok(yes)?$/.test(s));
    }
  });

  it('should support capture groups', function () {
    const re = /(foo)(bar)?/;
    for (let i = 0; i < 8; i++) {
      assert(/^(foo)(bar)?$/.test(new RandExp(re).gen()));
    }
  });
});