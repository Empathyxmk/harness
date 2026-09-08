const assert = require('assert');
const { stemmer } = require('../porter.js');

describe('Porter Stemmer - Branch Coverage Public Extra Tests', function() {
  it('should handle step 1b: eed but not mgr0 (public)', function() {
    assert.strictEqual(stemmer('bleed'), 'bleed');     // mgr0 false for 'ble'
    assert.strictEqual(stemmer('succeeded'), 'succeed');   // mgr0 true for 'succ'
  });

  it('should handle step 1b: ed/ing where no vowel in stem (public)', function() {
    assert.strictEqual(stemmer('ringed'), 'ring');    // vowel before 'ed'
    assert.strictEqual(stemmer('zzzzing'), 'zzzzing');  // no vowel before 'ing'
  });

  it('should handle step 1b: after removing ed/ing, "at"/"bl"/"iz" (public)', function() {
    assert.strictEqual(stemmer('clapping'), 'clap');
    assert.strictEqual(stemmer('buzzing'), 'buzz');
    assert.strictEqual(stemmer('kissing'), 'kiss');
    assert.strictEqual(stemmer('stalling'), 'stall');
  });

  it('should handle step 1c: y after vowel in stem (public)', function() {
    assert.strictEqual(stemmer('annoy'), 'annoi');
    assert.strictEqual(stemmer('toy'), 'toy');
  });

  it('should handle step 2: suffix not in list (public)', function() {
    assert.strictEqual(stemmer('happiest'), 'happiest');
    assert.strictEqual(stemmer('runniest'), 'runniest');
  });

  it('should handle step 3: suffix not in list (public)', function() {
    assert.strictEqual(stemmer('reactive'), 'reactiv');
  });

  it('should handle step 4: suffix not in list (public)', function() {
    assert.strictEqual(stemmer('lemonade'), 'lemonad');
  });

  it('should handle step 5a: ends with "e" and mgr1 regex (public)', function() {
    assert.strictEqual(stemmer('bake'), 'bake');
    assert.strictEqual(stemmer('debate'), 'debat');
  });

  it('should handle step 5b: double l after step 4 (public)', function() {
    assert.strictEqual(stemmer('compelled'), 'compel');
    assert.strictEqual(stemmer('expelled'), 'expel');
  });

  it('should return word unchanged if not matched in any step (public)', function() {
    assert.strictEqual(stemmer('qrp'), 'qrp');
  });
});