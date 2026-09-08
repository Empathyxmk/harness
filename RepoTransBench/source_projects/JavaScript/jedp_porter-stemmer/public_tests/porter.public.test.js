const assert = require('assert');
const { stemmer } = require('../porter.js');

describe('Porter Stemmer (Public Tests)', function() {
  it('stems regular plurals (public)', function() {
    assert.strictEqual(stemmer('buses'), 'bus');
    assert.strictEqual(stemmer('foxes'), 'fox');
    assert.strictEqual(stemmer('dishes'), 'dish');
    assert.strictEqual(stemmer('wishes'), 'wish');
    assert.strictEqual(stemmer('bats'), 'bat');
  });

  it('stems past tense (public)', function() {
    assert.strictEqual(stemmer('jumped'), 'jump');
    assert.strictEqual(stemmer('tangled'), 'tangl');
  });

  it('stems continuous verbs (public)', function() {
    assert.strictEqual(stemmer('running'), 'run');
    assert.strictEqual(stemmer('planned'), 'plan');
    assert.strictEqual(stemmer('dropping'), 'drop');
    assert.strictEqual(stemmer('buzzing'), 'buzz');
    assert.strictEqual(stemmer('jogged'), 'jog');
  });

  it('restores consonant-vowel-consonant when appropriate (public)', function() {
    assert.strictEqual(stemmer('filing'), 'file');
    assert.strictEqual(stemmer('begging'), 'beg');
  });

  it('handles y to i conversion (public)', function() {
    assert.strictEqual(stemmer('reply'), 'repli');
    assert.strictEqual(stemmer('apply'), 'appli');
  });

  it('handles step 2 replacements (public)', function() {
    assert.strictEqual(stemmer('national'), 'nation');
    assert.strictEqual(stemmer('organizational'), 'organiz');
    assert.strictEqual(stemmer('sensibility'), 'sensibl');
    assert.strictEqual(stemmer('responsiveness'), 'respons');
    assert.strictEqual(stemmer('formalize'), 'formal');
  });

  it('handles step 3 replacements (public)', function() {
    assert.strictEqual(stemmer('duplicate'), 'duplic');
    assert.strictEqual(stemmer('creative'), 'creat');
    assert.strictEqual(stemmer('playful'), 'play');
    assert.strictEqual(stemmer('fairness'), 'fair');
  });

  it('handles step 4 suffix removal (public)', function() {
    assert.strictEqual(stemmer('arrival'), 'arrival');
    assert.strictEqual(stemmer('performance'), 'perform');
    assert.strictEqual(stemmer('reference'), 'refer');
    assert.strictEqual(stemmer('machinist'), 'machinist');
    assert.strictEqual(stemmer('hydraulic'), 'hydraul');
    assert.strictEqual(stemmer('comfortable'), 'comfort');
    assert.strictEqual(stemmer('admissible'), 'admiss');
  });

  it('handles step 5a and 5b endings with "e" and "l" (public)', function() {
    assert.strictEqual(stemmer('refute'), 'refut');
    assert.strictEqual(stemmer('mute'), 'mute');
    assert.strictEqual(stemmer('arise'), 'aris');
    assert.strictEqual(stemmer('travell'), 'travel');
    assert.strictEqual(stemmer('toll'), 'toll');
  });

  it('returns unchanged for empty string and single-letter input (public)', function() {
    assert.strictEqual(stemmer(''), '');
    assert.strictEqual(stemmer('z'), 'z');
  });

  it('is idempotent (public)', function() {
    const word = 'dishes';
    assert.strictEqual(stemmer(word), stemmer(stemmer(word)));
  });
});