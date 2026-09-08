const frequencySort = require('./sort-characters-by-frequency');

// Helper to verify string frequencies
function stringHasFrequencies(res, freqObj) {
  const actualFreq = {};
  for (const ch of res) {
    actualFreq[ch] = (actualFreq[ch] || 0) + 1;
  }
  // Count check
  for (const k of Object.keys(freqObj)) {
    if (actualFreq[k] !== freqObj[k]) return false;
  }
  // All result chars must be in freqObj keys only
  for (const k of Object.keys(actualFreq)) {
    if (actualFreq[k] !== freqObj[k]) return false;
  }
  return true;
}

describe('frequencySort (public)', () => {
  test('example: s = "eefffggh"', () => {
    const res = frequencySort("eefffggh");
    // e:2, f:3, g:2, h:1. Any order as long as the higher-freqs come first.
    expect(res.length).toBe(8);
    expect(stringHasFrequencies(res, {e: 2, f: 3, g: 2, h: 1})).toBe(true);
    // first character must be 'f' (highest freq)
    expect(res[0]).toBe('f');
  });

  test('ties in character: s = "ppqqrr" (multiple 2s)', () => {
    const s = "ppqqrr";
    const res = frequencySort(s);
    expect(res.length).toBe(6);
    expect(stringHasFrequencies(res, {p:2,q:2,r:2})).toBe(true);
    // Check tie at beginning
    expect(['p','q','r']).toContain(res[0]);
  });

  test('s = "xyzxyzx"', () => {
    const res = frequencySort("xyzxyzx");
    // x:3, y:2, z:2
    expect(res.length).toBe(7);
    expect(stringHasFrequencies(res, {x:3, y:2, z:2})).toBe(true);
    expect(res[0]).toBe('x');
  });

  test('all unique', () => {
    // s = "klmnop" -> all freq 1
    const res = frequencySort("klmnop");
    expect(res.length).toBe(6);
    expect(stringHasFrequencies(res, {k:1, l:1, m:1, n:1, o:1, p:1})).toBe(true);
  });

  test('one char', () => {
    expect(frequencySort("z")).toBe("z");
  });

  test('mixed case', () => {
    // "CCDddcceeE": C:2, D:1, d:2, c:2, e:2, E:1
    const res = frequencySort("CCDddcceeE");
    expect(res.length).toBe(10);
    // C:2, D:1, d:2, c:2, e:2, E:1
    expect(stringHasFrequencies(res, {C:2, D:1, d:2, c:2, e:2, E:1})).toBe(true);
  });

  test('empty string', () => {
    expect(frequencySort("")).toBe("");
  });
});