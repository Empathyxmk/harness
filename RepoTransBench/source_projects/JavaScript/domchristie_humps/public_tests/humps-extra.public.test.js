const assert = require('assert');
const humps = require('../humps.js');

// ========== camelize ==========

describe('humps.js - extra/public utility & edge', function () {
  describe('camelize', function () {
    it('should handle strings with multiple delimiters', function () {
      assert.strictEqual(humps.camelize('bar_foo-baz quux'), 'barFooBazQuux');
    });
    it('should not alter numerical strings', function () {
      assert.strictEqual(humps.camelize('456'), '456');
    });
    it('should lowercase the first character', function () {
      // humps.camelize("TEST_CASE") returns 'tESTCASE'
      assert.strictEqual(humps.camelize('TEST_CASE'), 'tESTCASE');
    });
    it('should handle empty string', function () {
      assert.strictEqual(humps.camelize(''), '');
    });
  });

  describe('pascalize', function () {
    it('should capitalize the first letter', function () {
      assert.strictEqual(humps.pascalize('bar_foo'), 'BarFoo');
    });
    it('should handle camelCase', function () {
      assert.strictEqual(humps.pascalize('barFooBaz'), 'BarFooBaz');
    });
    it('should handle empty string', function () {
      assert.strictEqual(humps.pascalize(''), '');
    });
  });

  describe('decamelize', function () {
    it('should convert camelCase to snake_case', function () {
      assert.strictEqual(humps.decamelize('barFooBaz'), 'bar_foo_baz');
    });
    it('should use a custom separator', function () {
      // humps.decamelize('barFooBaz', '-') returns 'barfoobaz'
      assert.strictEqual(humps.decamelize('barFooBaz', '-'), 'barfoobaz');
    });
    it('should not change an already snake_cased string', function () {
      assert.strictEqual(humps.decamelize('bar_foo_baz'), 'bar_foo_baz');
    });
  });

  describe('_processKeys edge/types', function () {
    it('should return non-object values unchanged', function () {
      assert.strictEqual(humps.decamelizeKeys(5678), 5678);
      assert.strictEqual(humps.decamelizeKeys(null), null);
      assert.strictEqual(humps.decamelizeKeys(undefined), undefined);
      assert.strictEqual(humps.decamelizeKeys(false), false);
      assert.strictEqual(humps.decamelizeKeys(true), true);

      const d = new Date(2020, 1, 2);
      assert.strictEqual(humps.decamelizeKeys(d), d);
      
      const r = /def/;
      assert.strictEqual(humps.decamelizeKeys(r), r);
    });
    it('should return Dates unchanged except the key', function () {
      const d = new Date(2030, 5, 1);
      const obj = { someDate: d };
      const result = humps.decamelizeKeys(obj);
      assert.strictEqual(result.some_date, d);
    });

    it('should not alter RegExp, Boolean keys', function () {
      const r = /b/;
      const bool = false;
      const obj = { regExPattern: r, boolFlag: bool };
      const result = humps.decamelizeKeys(obj);
      assert.strictEqual(result.reg_ex_pattern, r);
      assert.strictEqual(result.bool_flag, bool);
    });

    it('should process prototype functions only if own property', function () {
      function Bar() {}
      Bar.prototype.protoMeth = function () { return 4; };
      Bar.prototype.protoAttr = 5;
      const b = new Bar();
      b.ownMeth = function () { return 5; };
      const hk = humps.camelizeKeys(b);
      assert('ownMeth' in hk);
      assert(!('protoMeth' in hk));
    });
    it('should process arrays', function () {
      assert.deepStrictEqual(humps.camelizeKeys([{bar_foo: 3}, {bar_baz: 4}]), [
        {barFoo: 3}, {barBaz: 4}
      ]);
    });
  });

  describe('pascalizeKeys, decamelizeKeys, depascalizeKeys', function () {
    it('should pascalize object keys recursively', function () {
      const o = { alpha_beta: { gamma_delta: 7 }};
      const r = humps.pascalizeKeys(o);
      assert('AlphaBeta' in r);
      assert('GammaDelta' in r.AlphaBeta);
    });
    it('should decamelizeKeys object keys', function () {
      const o = { alphaBeta: { gammaDelta: 7 }};
      const r = humps.decamelizeKeys(o);
      assert('alpha_beta' in r);
      assert('gamma_delta' in r.alpha_beta);
    });
    it('should depascalizeKeys (alias for decamelizeKeys)', function () {
      const o = { AlphaBeta: { GammaDelta: 7 }};
      const r = humps.depascalizeKeys(o);
      assert('alpha_beta' in r);
      assert('gamma_delta' in r.alpha_beta);
    });
    it('should decamelizeKeys with custom separator', function () {
      const o = { coolKey: 9, hotKey: 10 };
      const r = humps.decamelizeKeys(o, { separator: '.' });
      assert('cool.key' in r);
      assert('hot.key' in r);
    });
    it('should pascalizeKeys arrays', function () {
      const arr = [{alpha_beta: 123}];
      const r = humps.pascalizeKeys(arr);
      assert(Array.isArray(r));
      assert('AlphaBeta' in r[0]);
    });
  });

  describe('_processor and process callback', function () {
    it('should use custom process callback in options', function () {
      const obj = { alpha_beta: 88, gamma_delta: 77 };
      const opt = { process: k => 'x_' + k, recursive: true };
      const r = humps.camelizeKeys(obj, opt);
      assert('x_alpha_beta' in r);
      assert('x_gamma_delta' in r);
    });
    it('should fallback to convert if process is not a function', function () {
      const obj = { alpha_beta: 44 };
      const opt = { process: 0, recursive: true };
      const r = humps.camelizeKeys(obj, opt);
      assert('alphaBeta' in r);
    });
  });

  describe('module export (global/amd/require)', function() {
    it('should have camelize/decamelize/pascalize properties', function() {
      assert('camelize' in humps);
      assert('decamelize' in humps);
      assert('pascalize' in humps);
    });
  });
});