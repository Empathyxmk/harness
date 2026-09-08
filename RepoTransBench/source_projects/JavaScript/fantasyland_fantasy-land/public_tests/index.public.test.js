'use strict';

const assert = require('assert');
const path = require('path');
const fs = require('fs');

// Load the mapping using a relative path
const fantasyLand = require('../index.js');
const mappingKeys = Object.keys(fantasyLand);

// Alternate set of Fantasy Land keys for public test data (shuffled order and a new order)
const allPublicKeys = [
  'ap', 'equals', 'of', 'compose', 'contramap', 'traverse', 'map', 'extend',
  'concat', 'id', 'bimap', 'alt', 'reduce', 'extract', 'chain', 'lte',
  'filter', 'promap', 'invert', 'chainRec', 'empty', 'zero'
];

describe('FantasyLand mapping (public test) in CommonJS/Node', () => {
  it('exports all Fantasy Land mapping keys in public test order', () => {
    allPublicKeys.forEach((k) => {
      assert.ok(Object.prototype.hasOwnProperty.call(fantasyLand, k), `Missing key (public): ${k}`);
      assert.strictEqual(fantasyLand[k], 'fantasy-land/' + k);
    });
  });

  it('each key maps to the correct fantasy-land string (public test)', () => {
    allPublicKeys.forEach(key => {
      assert.strictEqual(fantasyLand[key], 'fantasy-land/' + key);
    });
  });

  it('contains all expected keys in a different order (public data)', () => {
    assert.deepStrictEqual(
      mappingKeys.slice().sort(),
      allPublicKeys.slice().sort(),
      'Mapping keys match Fantasy Land spec (public order, public data)'
    );
  });
});

describe('FantasyLand mapping (public) - type, value, and edge cases', () => {
  it('should contain only string values with different assertion order (public)', () => {
    allPublicKeys.forEach((key) => {
      const value = fantasyLand[key];
      assert.strictEqual(typeof value, 'string');
      assert.ok(value.endsWith('/' + key));
    });
  });

  it('should not contain duplicate values (public test)', () => {
    const values = Object.values(fantasyLand);
    const uniqueSet = new Set(values);
    assert.strictEqual(values.length, uniqueSet.size);
  });

  it('returns undefined for clearly fake keys (public test)', () => {
    assert.strictEqual(fantasyLand['this-is-not-a-key'], undefined);
    assert.strictEqual(fantasyLand['fantasy'], undefined);
    assert.strictEqual(fantasyLand['@@fantasy-land'], undefined);
  });

  it('public keys: all are present in the mapping (public test)', () => {
    allPublicKeys.forEach(key => {
      assert.ok(Object.prototype.hasOwnProperty.call(fantasyLand, key), `Public key ${key} is missing`);
    });
  });
});

describe('FantasyLand mapping (public) browser global fallback (simulated)', function () {
  it('assigns mapping to fake browser global self correctly (public version, shuffled keys)', function () {
    // Simulate a browser environment
    const context = { self: {} };
    const src = fs.readFileSync(path.join(__dirname, '..', 'index.js'), 'utf8');
    // Remove Node's module/exports from context to force the fallback branch
    const func = new Function('self', src + '; return self.FantasyLand;');
    const fantasyLandGlobal = func(context.self);
    allPublicKeys.forEach(key => {
      assert.strictEqual(fantasyLandGlobal[key], 'fantasy-land/' + key);
    });
  });
});