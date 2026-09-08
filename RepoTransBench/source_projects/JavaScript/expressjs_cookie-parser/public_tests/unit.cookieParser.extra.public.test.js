const assert = require('assert');
const cookieParser = require('../index');

// Patch to handle [Object: null prototype] returned by Object.create(null)
function normalize(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  return JSON.parse(JSON.stringify(obj));
}

describe('cookieParser (public)', function () {
  describe('signedCookies', function () {
    it('should decode signed cookies and remove from original (changed data)', function () {
      const cookies = { bar: 's:abcde' };
      const secrets = ['baz', 'qux'];
      const result = cookieParser.signedCookies({ bar: 's:12345.signature' }, 'baz');
      assert.deepStrictEqual(normalize(result), normalize({ bar: false }));
    });

    it('should return empty object if no signed cookies (changed data)', function () {
      const result = cookieParser.signedCookies({ foo: 'plain' }, 'baz');
      assert.deepStrictEqual(normalize(result), normalize({}));
    });

    it('should work with empty input (public variant)', function () {
      const result = cookieParser.signedCookies({}, 'quux');
      assert.deepStrictEqual(normalize(result), normalize({}));
    });
  });

  describe('cookieParser() internal', function () {
    it('should populate req.cookies and req.signedCookies for empty cookies (public)', function () {
      const req = { headers: { cookie: '' } };
      const res = {};
      const next = function () {
        assert.deepStrictEqual(normalize(req.cookies), normalize({}));
        assert.deepStrictEqual(normalize(req.signedCookies), normalize({}));
      };
      cookieParser()(req, res, next);
    });
  });
});