const stringSimilarity = require('../src/index');

describe('Extra Coverage for string-similarity (public tests)', () => {
  describe('findBestMatch', () => {
    it('should handle identical strings', () => {
      const result = stringSimilarity.findBestMatch('goodbye', ['goodbye', 'cruel world']);
      expect(result.bestMatch.target).toEqual('goodbye');
      expect(result.ratings[0].rating).toBeCloseTo(1);
    });

    it('should handle non-string input', () => {
      expect(() => stringSimilarity.findBestMatch(undefined, ['xyz'])).toThrow();
      expect(() => stringSimilarity.findBestMatch(null, ['xyz'])).toThrow();
      expect(() => stringSimilarity.findBestMatch('xyz', [undefined])).toThrow();
    });

    it('should give best match from possible ties', () => {
      const targets = ['tie', 'tie', 'untie'];
      const input = 'tie';
      const result = stringSimilarity.findBestMatch(input, targets);
      expect(result.bestMatch.target).toEqual('tie');
      expect(result.ratings.filter(r => r.rating === 1).length).toBeGreaterThan(0);
    });

    it('should handle similar non-equal multi-word strings', () => {
      const input = 'baz foo bar';
      const options = ['baz foo jar', 'foo bar', 'bar baz boo'];
      const result = stringSimilarity.findBestMatch(input, options);
      expect(options).toContain(result.bestMatch.target);
    });
  });
});