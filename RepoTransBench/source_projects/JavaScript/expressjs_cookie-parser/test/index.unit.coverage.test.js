// --- Amend ONLY the failing test ---

const assert = require('assert');
const cookieParser = require('../index');
const { signedCookies } = require('../index');

describe('signedCookies', function () {
  it('should decode signed cookies and remove from original object (fixed for null prototype)', function () {
    // Arrange: 'b' is a signed ("s:") cookie (invalid), 'a' is just plain value.
    let obj = Object.create(null);
    obj.a = 'val';
    obj.b = 's:val.signature';
    // According to implementation, signed cookies that fail verification become 'false'
    // Output should be an object with null prototype, { b: false }
    const secrets = ['keyboard cat'];
    const decoded = signedCookies(obj, secrets);
    assert.strictEqual(Object.getPrototypeOf(decoded), null, 'Prototype is not null');
    // For deepStrictEqual with null proto objects, must construct match object:
    const expected = Object.create(null);
    expected.b = false;
    assert.deepStrictEqual(decoded, expected);
  });

  it('should return empty object if no signed values (fixed for null prototype)', function () {
    let obj = Object.create(null);
    obj.a = 'val';
    const secrets = ['keyboard cat'];
    const result = signedCookies(obj, secrets);
    assert.strictEqual(Object.getPrototypeOf(result), null, 'Prototype is not null');
    // No signed cookies -> empty object with null prototype
    assert.deepStrictEqual(result, Object.create(null));
  });
});

describe('cookieParser middleware edge cases', function () {
  it('should handle no cookies case (fixed for null prototype)', function (done) {
    // The req.headers property must exist, even if empty.
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