const assert = require('assert');
const cookieParser = require('../index');
const { signedCookies } = require('../index');

describe('signedCookies (public)', function () {
  it('should decode signed cookies and remove from original object, public data', function () {
    // Arrange: 'c' is a signed ("s:") cookie (invalid), 'd' is just plain value.
    let obj = Object.create(null);
    obj.d = 'xyz';
    obj.c = 's:data.nope';
    const secrets = ['secret squirrel'];
    const decoded = signedCookies(obj, secrets);
    assert.strictEqual(Object.getPrototypeOf(decoded), null, 'Prototype is not null');
    const expected = Object.create(null);
    expected.c = false;
    assert.deepStrictEqual(decoded, expected);
  });

  it('should return empty object if no signed values (different data)', function () {
    let obj = Object.create(null);
    obj.e = 'plain';
    const secrets = ['another secret'];
    const result = signedCookies(obj, secrets);
    assert.strictEqual(Object.getPrototypeOf(result), null, 'Prototype is not null');
    assert.deepStrictEqual(result, Object.create(null));
  });
});

describe('cookieParser middleware edge cases (public)', function () {
  it('should handle no cookies case with different req.headers (public)', function (done) {
    const req = { headers: {} };
    const res = {};
    const next = function () {
      assert.strictEqual(Object.getPrototypeOf(req.cookies), null, 'Prototype is not null');
      assert.deepStrictEqual(req.cookies, Object.create(null));
      done();
    };
    cookieParser()(req, res, next);
  });
});