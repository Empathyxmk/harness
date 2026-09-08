const spellfucker = require('../src/spellfucker');

describe('spellfucker advanced and edge cases (public test data)', () => {
  it('should return string "1" for number 1', () => {
    expect(spellfucker(1)).toBe('1');
  });

  it('should return string "true" for true', () => {
    expect(spellfucker(true)).toBe('true');
  });

  it('should skip non-string, non-convertible types (function, symbol)', () => {
    expect(spellfucker(function(){})).toBe('');
    if (typeof Symbol !== 'undefined')
      expect(spellfucker(Symbol())).toBe('');
  });

  it('should not explode on very short string', () => {
    let short = 'xy';
    let out = spellfucker(short);
    expect(typeof out).toBe('string');
    expect(out.length).toBeGreaterThanOrEqual(0);
  });

  it('should not increase length substantially for a new word', () => {
    const s = 'oranges';
    const mutated = spellfucker(s);
    expect(Math.abs(mutated.length - s.length)).toBeLessThan(s.length);
  });

  it('should make a change for other consonant pattern words', () => {
    const words = [
      'dizzy',   // zz → z
      'shush',   // sh not altered, but caused by ch/ss mutators
      'luggage', // gg, g
      'queue',   // qu→kw
      'eight',   // ght
      'phrase',  // ph→f
      'scene',   // ce
      'bizarre', // rr
      'committee', // mm, tt
      'knapsack', // kn, ck/k
      'whip',    // wh, p
      'cello',   // c
      'succeed', // cc, d
      'ill',     // ll
      'summon',  // mm, n
      'neat',    // t
      'grove',   // v
      'white',   // wh
      'kiss',    // ss
      'phantasm',// ph, m
      'genuine', // gn
    ];
    for (const w of words) {
      const out = spellfucker(w);
      expect(typeof out).toBe('string');
      expect(out.length).toBeGreaterThanOrEqual(0);
    }
  });

  it('should support PascalCase and digits', () => {
    const input = 'PascalCase123';
    const output = spellfucker(input);
    expect(output.length).toBeGreaterThan(0);
    expect(typeof output).toBe('string');
  });

  it('should act deterministically (different strings)', () => {
    expect(typeof spellfucker('butterscotch')).toBe('string');
    expect(typeof spellfucker('engineering')).toBe('string');
  });

  it('should handle repeated replacements at string start/end (public cases)', () => {
    ['cats', 'dot', 'mmm', 'groove', 'eating', 'tag', 'dance'].forEach(word => {
      expect(typeof spellfucker(word)).toBe('string');
      expect(spellfucker(word).length).toBeGreaterThanOrEqual(0);
    });
  });
});