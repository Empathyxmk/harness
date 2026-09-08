const fs = require('fs');
const path = require('path');

const WORDS_FILE = path.join(__dirname, 'test_words_public.txt');
// New text for public tests: different words, different frequency profile, mixed case, extra word
const WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow';

beforeAll(() => {
  fs.writeFileSync(WORDS_FILE, WORDS_TEXT, 'utf8');
});

afterAll(() => {
  fs.unlinkSync(WORDS_FILE);
});

describe('WordCount Class (public tests, 3.oo-one-class.js)', () => {
  const WordCount = require('../3.oo-one-class.js.tmp.js');

  it('should read file content correctly (public)', () => {
    const wc = new WordCount(WORDS_FILE);
    expect(wc.content()).toBe(WORDS_TEXT);
  });

  it('should split words properly and avoid empty strings (public)', () => {
    const wc = new WordCount(WORDS_FILE);
    expect(wc.words()).toEqual([
      'Red', 'red', 'Blue', 'blue', 'blue', 'Green', 'green', 'yellow', 'yellow', 'yellow'
    ]);
  });

  it('should handle empty file gracefully (public)', () => {
    const EMPTY_FILE = path.join(__dirname, 'empty_public.txt');
    fs.writeFileSync(EMPTY_FILE, '', 'utf8');
    const wc = new WordCount(EMPTY_FILE);
    expect(wc.words()).toEqual(['']);
    expect(wc.tally()).toHaveProperty('', 1);
    fs.unlinkSync(EMPTY_FILE);
  });

  it('should tally words case-insensitively (public)', () => {
    const wc = new WordCount(WORDS_FILE);
    const tally = wc.tally();
    expect(tally).toHaveProperty('blue', 3);
    expect(tally).toHaveProperty('red', 2);
    expect(tally).toHaveProperty('green', 2);
    expect(tally).toHaveProperty('yellow', 3);
  });

  it('should return top 10 entries (all in this case, public)', () => {
    const wc = new WordCount(WORDS_FILE);
    const top = wc.top10();
    expect(top[0].word).toBe('blue');
    expect(top[0].count).toBe(3);
    expect(top.map(e => e.word)).toContain('red');
    expect(top.map(e => e.word)).toContain('green');
    expect(top.map(e => e.word)).toContain('yellow');
  });

  it('should handle ties in top10 (public, tie for 2 each)', () => {
    const FILE = path.join(__dirname, 'ties_public.txt');
    fs.writeFileSync(FILE, 'alpha beta alpha beta gamma', 'utf8');
    const wc = new WordCount(FILE);
    const top = wc.top10();
    expect(top[0].count).toBe(2);
    expect(top[1].count).toBe(2);
    fs.unlinkSync(FILE);
  });

  it('should printTop10 as expected (public)', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const wc = new WordCount(WORDS_FILE);
    wc.printTop10();
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });

  it('main should run without throwing (public)', () => {
    expect(() => WordCount.main(WORDS_FILE)).not.toThrow();
  });

  it('top10 returns no more than 10 results (public)', () => {
    const FILE = path.join(__dirname, 'tenplus_public.txt');
    fs.writeFileSync(FILE, Array.from({length: 12}).map((_, i) => `p${i}`).join(' '), 'utf8');
    const wc = new WordCount(FILE);
    expect(wc.top10().length).toBe(10);
    fs.unlinkSync(FILE);
  });
});