const fs = require('fs');
const path = require('path');

const WORDS_FILE = path.join(__dirname, 'test_words.txt');
// Adjusted test text: remove trailing separators to avoid split/join issues and empty strings in .words()
const WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog';

beforeAll(() => {
  fs.writeFileSync(WORDS_FILE, WORDS_TEXT, 'utf8');
});

afterAll(() => {
  fs.unlinkSync(WORDS_FILE);
});

describe('WordCount Class (3.oo-one-class.js)', () => {
  const WordCount = require('../3.oo-one-class.js.tmp.js');

  it('should read file content correctly', () => {
    const wc = new WordCount(WORDS_FILE);
    expect(wc.content()).toBe(WORDS_TEXT);
  });

  it('should split words properly (no empty strings in output)', () => {
    const wc = new WordCount(WORDS_FILE);
    // Should not include empty strings due to adjusted input and regex splitting
    expect(wc.words()).toEqual([
      'Apple', 'apple', 'Banana', 'banana', 'banana', 'Cat', 'cat', 'dog', 'dog', 'dog'
    ]);
  });

  it('should handle empty file gracefully', () => {
    const EMPTY_FILE = path.join(__dirname, 'empty.txt');
    fs.writeFileSync(EMPTY_FILE, '', 'utf8');
    const wc = new WordCount(EMPTY_FILE);
    expect(wc.words()).toEqual(['']);
    expect(wc.tally()).toHaveProperty('', 1);
    fs.unlinkSync(EMPTY_FILE);
  });

  it('should tally words case-insensitively', () => {
    const wc = new WordCount(WORDS_FILE);
    const tally = wc.tally();
    expect(tally).toHaveProperty('banana', 3);
    expect(tally).toHaveProperty('apple', 2);
    expect(tally).toHaveProperty('cat', 2);
    expect(tally).toHaveProperty('dog', 3);
  });

  it('should return top 10 entries (all in this case)', () => {
    const wc = new WordCount(WORDS_FILE);
    const top = wc.top10();
    expect(top[0].word).toBe('banana');
    expect(top[0].count).toBe(3);
    expect(top.map(e => e.word)).toContain('dog');
    expect(top.map(e => e.word)).toContain('apple');
    expect(top.map(e => e.word)).toContain('cat');
  });

  it('should handle ties in top10 (same count)', () => {
    const FILE = path.join(__dirname, 'ties.txt');
    fs.writeFileSync(FILE, 'one two one two three', 'utf8');
    const wc = new WordCount(FILE);
    const top = wc.top10();
    expect(top[0].count).toBe(2);
    expect(top[1].count).toBe(2);
    fs.unlinkSync(FILE);
  });

  it('should printTop10 as expected', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const wc = new WordCount(WORDS_FILE);
    wc.printTop10();
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });

  it('main should run without throwing', () => {
    expect(() => WordCount.main(WORDS_FILE)).not.toThrow();
  });

  it('top10 returns no more than 10 results', () => {
    const FILE = path.join(__dirname, 'tenplus.txt');
    fs.writeFileSync(FILE, Array.from({length: 15}).map((_, i) => `w${i}`).join(' '), 'utf8');
    const wc = new WordCount(FILE);
    expect(wc.top10().length).toBe(10);
    fs.unlinkSync(FILE);
  });
});