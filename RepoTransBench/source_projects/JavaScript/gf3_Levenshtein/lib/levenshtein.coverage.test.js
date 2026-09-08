// This test aims for branch and line coverage on lib/levenshtein.js

const levenshtein = require('./levenshtein');

// Test: identical strings
test('levenshtein identical strings', () => {
  expect(levenshtein('abc', 'abc')).toBe(0);
});

// Test: completely different strings
test('levenshtein completely different strings', () => {
  expect(levenshtein('abc', 'xyz')).toBe(3);
});

// Test: substrings
test('levenshtein with substring', () => {
  expect(levenshtein('kitten', 'kit')).toBe(3);
  expect(levenshtein('kit', 'kitten')).toBe(3);
});

// Test: empty string cases
test('levenshtein with one empty', () => {
  expect(levenshtein('', 'abc')).toBe(3);
  expect(levenshtein('abc', '')).toBe(3);
});

// Test: both empty
test('levenshtein with both empty', () => {
  expect(levenshtein('', '')).toBe(0);
});

// Test: single char difference
test('levenshtein single replace', () => {
  expect(levenshtein('a', 'b')).toBe(1);
});

// Test: add, delete, replace
test('levenshtein add/delete/replace', () => {
  expect(levenshtein('abc', 'ab')).toBe(1); // delete
  expect(levenshtein('ab', 'abc')).toBe(1); // add
  expect(levenshtein('abc', 'adc')).toBe(1); // replace
  expect(levenshtein('abc', 'axc')).toBe(1); // replace
  expect(levenshtein('abcdef', 'azced')).toBe(3); // complex
});

// Test: equal length but different
test('levenshtein equal length totally different', () => {
  expect(levenshtein('cat', 'dog')).toBe(3);
});

// Test: Unicode
test('levenshtein unicode', () => {
  expect(levenshtein('mañana', 'manana')).toBe(1);
  expect(levenshtein('🙂', '🙃')).toBe(1);
});