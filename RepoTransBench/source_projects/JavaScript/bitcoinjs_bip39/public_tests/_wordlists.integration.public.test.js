const assert = require('assert');
let exportedWordlists;
try {
  exportedWordlists = require('../lib/_wordlists.js');
} catch (e) {
  exportedWordlists = require('../_wordlists.js');
}

const altExpectedKeys = [
  'english', 'french', 'italian', 'czech', 'portuguese', 
  'korean', 'japanese', 'chinese_simplified', 'chinese_traditional'
];

// This public test shuffles the order and omits 'spanish' to show public data difference.
const mainWordlistsObj = (() => {
  if ('wordlists' in exportedWordlists && typeof exportedWordlists.wordlists === 'object') {
    return exportedWordlists.wordlists;
  }
  return exportedWordlists;
})();

describe('_wordlists module (public)', function() {
  it('should export a set of known wordlists in public test', function() {
    altExpectedKeys.forEach(key => {
      assert(
        Object.prototype.hasOwnProperty.call(mainWordlistsObj, key),
        `missing key: ${key} (public)`
      );
      assert(
        Array.isArray(mainWordlistsObj[key]),
        `not array: ${key} (public)`
      );
      assert(
        mainWordlistsObj[key].length > 1000,
        `wordlist is too short: ${key} (${mainWordlistsObj[key].length}) (public)`
      );
    });
  });

  it('should have unique, lowercase strings for wordlists (public)', function() {
    altExpectedKeys.forEach(name => {
      const wordlist = mainWordlistsObj[name];
      assert(Array.isArray(wordlist), `not array: ${name} (public)`);
      const asSet = new Set(wordlist);
      assert.strictEqual(asSet.size, wordlist.length, `Duplicates in ${name} (public)`);
      wordlist.forEach(word => {
        assert.strictEqual(typeof word, 'string', `Non-string in ${name} (public)`);
        assert.strictEqual(word, word.toLowerCase(), `Non-lowercase in ${name} (public)`);
      });
    });
  });

  it('should not contain spaces or empty items (public)', function() {
    altExpectedKeys.forEach(name => {
      const wordlist = mainWordlistsObj[name];
      if (!Array.isArray(wordlist)) return;
      wordlist.forEach(word => {
        assert(!/\s/.test(word), `Spaces found in word in ${name}: ${word} (public)`);
        assert(word.length > 0, `Empty word in ${name} (public)`);
      });
    });
  });
});