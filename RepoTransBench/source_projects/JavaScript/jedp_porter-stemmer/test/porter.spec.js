const assert = require('assert');
const { stemmer } = require('../porter.js');

describe('Porter Stemmer', function() {
  it('stems regular plurals', function() {
    assert.strictEqual(stemmer('caresses'), 'caress');
    assert.strictEqual(stemmer('ponies'), 'poni');
    assert.strictEqual(stemmer('ties'), 'ti');
    assert.strictEqual(stemmer('caress'), 'caress');
    assert.strictEqual(stemmer('cats'), 'cat');
  });

  it('stems past tense', function() {
    assert.strictEqual(stemmer('agreed'), 'agre');
    assert.strictEqual(stemmer('disabled'), 'disabl');
  });

  it('stems continuous verbs', function() {
    assert.strictEqual(stemmer('hopping'), 'hop');
    assert.strictEqual(stemmer('tanned'), 'tan');
    assert.strictEqual(stemmer('falling'), 'fall');
    assert.strictEqual(stemmer('hissing'), 'hiss');
    assert.strictEqual(stemmer('fizzed'), 'fizz');
  });

  it('restores consonant-vowel-consonant when appropriate', function() {
    assert.strictEqual(stemmer('filing'), 'file');
    assert.strictEqual(stemmer('sing'), 'sing');
  });

  it('handles y to i conversion', function() {
    assert.strictEqual(stemmer('cry'), 'cry');
    assert.strictEqual(stemmer('sky'), 'sky');
  });

  it('handles step 2 replacements', function() {
    assert.strictEqual(stemmer('relational'), 'relat');
    assert.strictEqual(stemmer('conditional'), 'condit');
    assert.strictEqual(stemmer('rational'), 'ration');
    assert.strictEqual(stemmer('valency'), 'valenc');
    assert.strictEqual(stemmer('digitizer'), 'digit');
  });

  it('handles step 3 replacements', function() {
    assert.strictEqual(stemmer('triplicate'), 'triplic');
    assert.strictEqual(stemmer('formative'), 'form');
    assert.strictEqual(stemmer('hopeful'), 'hope');
    assert.strictEqual(stemmer('goodness'), 'good');
  });

  it('handles step 4 suffix removal', function() {
    assert.strictEqual(stemmer('revival'), 'reviv');
    assert.strictEqual(stemmer('allowance'), 'allow');
    assert.strictEqual(stemmer('inference'), 'infer');
    assert.strictEqual(stemmer('airliner'), 'airlin');
    assert.strictEqual(stemmer('gyroscopic'), 'gyroscop');
    assert.strictEqual(stemmer('adjustable'), 'adjust');
    assert.strictEqual(stemmer('defensible'), 'defens');
  });

  it('handles step 5a and 5b endings with "e" and "l"', function() {
    assert.strictEqual(stemmer('probate'), 'probat');
    assert.strictEqual(stemmer('rate'), 'rate');
    assert.strictEqual(stemmer('cease'), 'ceas');
    assert.strictEqual(stemmer('controll'), 'control');
    assert.strictEqual(stemmer('roll'), 'roll');
  });

  it('returns unchanged for empty string and single-letter input', function() {
    assert.strictEqual(stemmer(''), '');
    assert.strictEqual(stemmer('a'), 'a');
  });

  it('is idempotent', function() {
    const word = 'caresses';
    assert.strictEqual(stemmer(word), stemmer(stemmer(word)));
  });
});