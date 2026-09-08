const assert = require('assert');
let exportedWordlists;
try {
  exportedWordlists = require('../lib/_wordlists.js');
} catch (e) {
  exportedWordlists = require('../_wordlists.js');
}

const expectedKeys = [
  'english', 'japanese', 'chinese_simplified', 'chinese_traditional',
  'french', 'italian', 'spanish', 'czech', 'korean', 'portuguese'
];

// Some bip39 implementations export {wordlists: {english: [...], ...}, ...}
const mainWordlistsObj = (() => {
  // If a wrapping "wordlists" object, use that. Otherwise, use the main export.
  if ('wordlists' in exportedWordlists && typeof exportedWordlists.wordlists === 'object') {
    return exportedWordlists.wordlists;
  }
  return exportedWordlists;
})();

describe('_wordlists module', function() {
  it('should export all expected wordlists', function() {
    expectedKeys.forEach(key => {
      assert(
        Object.prototype.hasOwnProperty.call(mainWordlistsObj, key),
        `missing key: ${key}`
      );
      assert(
        Array.isArray(mainWordlistsObj[key]),
        `not array: ${key}`
      );
      assert(
        mainWordlistsObj[key].length > 1000,
        `wordlist is too short: ${key} (${mainWordlistsObj[key].length})`
      );
    });
  });

  it('should have all wordlists with unique, lowercase strings', function() {
    expectedKeys.forEach(name => {
      const wordlist = mainWordlistsObj[name];
      assert(Array.isArray(wordlist), `not array: ${name}`);
      const asSet = new Set(wordlist);
      assert.strictEqual(asSet.size, wordlist.length, `Duplicates in ${name}`);
      wordlist.forEach(word => {
        assert.strictEqual(typeof word, 'string', `Non-string in ${name}`);
        assert.strictEqual(word, word.toLowerCase(), `Non-lowercase in ${name}`);
      });
    });
  });

  it('should not contain obvious garbage', function() {
    expectedKeys.forEach(name => {
      const wordlist = mainWordlistsObj[name];
      if (!Array.isArray(wordlist)) return;
      wordlist.forEach(word => {
        assert(!/\s/.test(word), `Spaces found in word in ${name}: ${word}`);
        assert(word.length > 0, `Empty word in ${name}`);
      });
    });
  });
});