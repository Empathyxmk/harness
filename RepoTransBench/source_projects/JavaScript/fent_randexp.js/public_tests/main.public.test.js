const assert = require('assert');
const RandExp = require('../lib/randexp');

describe('RandExp basic and advanced usage (PUBLIC)', function () {
  it('should generate a string that matches a new RegExp', function () {
    const re = /^A\d{2}Z$/;
    for (let i = 0; i < 10; ++i) {
      const s = new RandExp(re).gen();
      assert(re.test(s), `Result "${s}" does not match ${re}`);
      assert(s[0] === 'A' && s.slice(-1) === 'Z');
    }
  });

  it('should generate digits with word boundaries', function () {
    const re = /\b\d{3}\b/;
    for (let i = 0; i < 10; ++i) {
      const s = new RandExp(re).gen();
      assert(/^\d{3}$/.test(s), `Got "${s}"`);
    }
  });

  it('should generate alternative branches', function () {
    const re = /cat|bat|rat/;
    const options = ["cat", "bat", "rat"];
    for (let i = 0; i < 5; ++i) {
      const s = new RandExp(re).gen();
      assert(options.includes(s));
    }
  });
});