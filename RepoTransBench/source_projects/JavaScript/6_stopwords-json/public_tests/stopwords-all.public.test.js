const assert = require('chai').assert;
const stopwordsData = require('../stopwords-all.json');

describe('stopwords-all.json public tests', function () {
  it('should contain stopwords for a different valid language (e.g., "fr") and check inclusion of a known French stopword', function () {
    assert.property(stopwordsData, 'fr');
    assert.include(stopwordsData['fr'], 'dans'); // 'dans' is a French stopword not identical to common first entry in lists
  });

  it('should contain stopwords for another language (e.g., "sv") and check for typical Swedish stopword', function () {
    assert.property(stopwordsData, 'sv');
    assert.include(stopwordsData['sv'], 'och'); // 'och' means 'and' in Swedish, a common stopword
  });

  it('should have a non-empty array for a lesser-used language (e.g., "eo") and check a typical Esperanto stopword', function () {
    assert.property(stopwordsData, 'eo');
    assert.isArray(stopwordsData['eo']);
    assert.include(stopwordsData['eo'], 'kaj'); // 'kaj' means 'and' in Esperanto
  });

  it('should support a language from the asp-stoplist-project (e.g., "yo") and check for a Yoruba stopword', function () {
    assert.property(stopwordsData, 'yo');
    assert.include(stopwordsData['yo'], 'ati'); // 'ati' is a common Yoruba stopword
  });
});