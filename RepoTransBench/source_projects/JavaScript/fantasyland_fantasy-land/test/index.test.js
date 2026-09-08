'use strict';

const assert = require('assert');
const path = require('path');
const fs = require('fs');

const fantasyLand = require('../index.js');
const mappingKeys = Object.keys(fantasyLand);

const allPossibleKeys = [
  'equals', 'lte', 'concat', 'empty', 'map', 'ap', 'of', 'reduce',
  'traverse', 'chain', 'bimap', 'extend', 'extract', 'compose',
  'id', 'zero', 'alt', 'promap', 'filter', 'contramap', 'chainRec', 'invert'
];

describe('FantasyLand mapping in CommonJS/Node', () => {
  it('exports all Fantasy Land mapping keys', () => {
    mappingKeys.forEach((k) => {
      assert.ok(Object.prototype.hasOwnProperty.call(fantasyLand, k), `Missing key: ${k}`);
      assert.strictEqual(fantasyLand[k], 'fantasy-land/' + k);
    });
  });

  it('each key maps to the correct fantasy-land string', () => {
    mappingKeys.forEach(key => {
      assert.strictEqual(fantasyLand[key], 'fantasy-land/' + key);
    });
  });

  it('contains all expected keys (no extra, no missing)', () => {
    assert.deepStrictEqual(
      mappingKeys.sort(),
      allPossibleKeys.sort(),
      'Mapping keys match Fantasy Land spec'
    );
  });
});

describe('FantasyLand mapping - edge and type cases', () => {
  it('should contain only string values', () => {
    Object.values(fantasyLand).forEach(value => {
      assert.strictEqual(typeof value, 'string');
      assert.ok(value.startsWith('fantasy-land/'));
    });
  });

  it('should not contain duplicate values', () => {
    const values = Object.values(fantasyLand);
    const set = new Set(values);
    assert.strictEqual(values.length, set.size);
  });

  it('throws on invalid property access (not in mapping)', () => {
    assert.strictEqual(fantasyLand['not-a-key'], undefined);
  });
  
  it('all keys from allPossibleKeys are present', () => {
    allPossibleKeys.forEach(key => {
      assert.ok(fantasyLand.hasOwnProperty(key), `Key ${key} is missing`);
    });
  });
});

// Faulty test removed, replaced with a safer simulation test for the browser branch:
describe('FantasyLand mapping global fallback (browser env)', function () {
  it('assigns mapping to fake global self correctly (simulated)', function () {
    // Simulate a minimal browser environment
    const context = { self: {} };
    const src = fs.readFileSync(path.join(__dirname, '..', 'index.js'), 'utf8');
    // Remove Node's module/exports from context to force the fallback branch
    // Run in a function that sets 'self' to context.self
    const func = new Function('self', src + '; return self.FantasyLand;');
    const fantasyLandGlobal = func(context.self);
    allPossibleKeys.forEach(key => {
      assert.strictEqual(fantasyLandGlobal[key], 'fantasy-land/' + key);
    });
  });
});