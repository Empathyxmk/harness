const assert = require('assert');
const { stemmer } = require('../porter.js');

// Fix: Correct test expectation for "enjoy" - Porter stemmer should convert "enjoy" to "enjoi" in step 1c

describe('Porter Stemmer - Branch Coverage Extra Tests', function() {
  it('should handle step 1b: eed but not mgr0', function() {
    assert.strictEqual(stemmer('feed'), 'feed');     // mgr0 false for 'fe'
    assert.strictEqual(stemmer('agreed'), 'agre');   // mgr0 true for 'agr'
  });

  it('should handle step 1b: ed/ing where no vowel in stem', function() {
    assert.strictEqual(stemmer('singed'), 'sing');    // vowel before 'ed'
    assert.strictEqual(stemmer('zzzing'), 'zzzing');  // no vowel before 'ing'
  });

  it('should handle step 1b: after removing ed/ing, "at"/"bl"/"iz"', function() {
    assert.strictEqual(stemmer('hopping'), 'hop');
    assert.strictEqual(stemmer('fizzing'), 'fizz');
    assert.strictEqual(stemmer('hissing'), 'hiss');
    assert.strictEqual(stemmer('falling'), 'fall');
  });

  it('should handle step 1c: y after vowel in stem', function() {
    assert.strictEqual(stemmer('enjoy'), 'enjoi'); // Fix: expecting "enjoi", not "enjoy"
    assert.strictEqual(stemmer('cry'), 'cry');
  });

  it('should handle step 2: suffix not in list', function() {
    assert.strictEqual(stemmer('happily'), 'happili');
    assert.strictEqual(stemmer('runningly'), 'runningli');
  });

  it('should handle step 3: suffix not in list', function() {
    assert.strictEqual(stemmer('proactive'), 'proactiv');
  });

  it('should handle step 4: suffix not in list', function() {
    assert.strictEqual(stemmer('marathon'), 'marathon');
  });

  it('should handle step 5a: ends with "e" and mgr1 regex', function() {
    assert.strictEqual(stemmer('cite'), 'cite');
    assert.strictEqual(stemmer('abate'), 'abat');
  });

  it('should handle step 5b: double l after step 4', function() {
    assert.strictEqual(stemmer('controlled'), 'control');
    assert.strictEqual(stemmer('rolled'), 'roll');
  });

  it('should return word unchanged if not matched in any step', function() {
    assert.strictEqual(stemmer('xyz'), 'xyz');
  });
});