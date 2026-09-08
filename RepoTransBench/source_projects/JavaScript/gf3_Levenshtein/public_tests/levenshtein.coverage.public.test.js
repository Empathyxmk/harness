const levenshtein = require('../lib/levenshtein');

// Test: Empty strings (remain unchanged)
test('levenshtein empty strings (public)', () => {
  expect(levenshtein('', '')).toBe(0);
  expect(levenshtein('abc', '')).toBe(3);
  expect(levenshtein('', 'xyz')).toBe(3);
});

// Test: same value
test('levenshtein identical strings (public)', () => {
  expect(levenshtein('good', 'good')).toBe(0);
});

// Test: insertions
test('levenshtein pure insert (public)', () => {
  expect(levenshtein('red', 'ready')).toBe(2);
  expect(levenshtein('go', 'gone')).toBe(2);
});

// Test: deletions
test('levenshtein pure delete (public)', () => {
  expect(levenshtein('testing', 'test')).toBe(3);
});

// Test: substitutions
test('levenshtein substitution (public)', () => {
  expect(levenshtein('like', 'bike')).toBe(1);
});

// Test: basic difference
test('levenshtein simple diff (public)', () => {
  expect(levenshtein('hat', 'what')).toBe(1);
});

// Test: one char off, equal length
test('levenshtein single substitution equal length (public)', () => {
  expect(levenshtein('glass', 'grass')).toBe(1);
});

// Test: two insertions
test('levenshtein double insertion (public)', () => {
  expect(levenshtein('sing', 'signal')).toBe(3);
});

// Test: swap characters
test('levenshtein swapped characters (public)', () => {
  expect(levenshtein('form', 'from')).toBe(2);
});

// Test: equal length but totally different
test('levenshtein equal length totally different (public)', () => {
  // 'car' and 'dog': all chars completely different, distance = 3
  expect(levenshtein('car', 'dog')).toBe(3);
});

// Test: Unicode
test('levenshtein unicode (public)', () => {
  // 'mañana' vs 'manana' (ñ vs n): 1 change
  expect(levenshtein('mañana', 'manana')).toBe(1);
  // Emoji difference
  expect(levenshtein('🏀', '⚽️')).toBe(2);
});