const fs = require('fs');
const path = require('path');

const WORDS_FILE = path.join(__dirname, 'test_words2.txt');
const WORDS_TEXT = 'one two two, three. three three. four four four four';

beforeAll(() => {
  fs.writeFileSync(WORDS_FILE, WORDS_TEXT, 'utf8');
});

afterAll(() => {
  fs.unlinkSync(WORDS_FILE);
});

describe('4.oo-small-classes.js classes', () => {
  const { Tokenizer, FileReader, Tally, Top10Printer, WordCount } = require('../4.oo-small-classes.js.tmp.js'); // We'll need to export these

  test('Tokenizer splits correctly', () => {
    const t = new Tokenizer();
    expect(t.tokenize('alpha beta,gamma')).toEqual(['alpha', 'beta', 'gamma']);
  });

  test('FileReader reads text and words', () => {
    const fr = new FileReader(WORDS_FILE);
    expect(fr.read()).toBe(WORDS_TEXT);
    expect(fr.readWords()).toContain('three');
  });

  test('Tally tallies, sorts, slices correctly', () => {
    const fr = new FileReader(WORDS_FILE);
    const tally = new Tally(fr.readWords());
    expect(tally.tally['three']).toBe(3);
    expect(tally.tally['four']).toBe(4);
    expect(tally.getTop10()[0]).toEqual({ word: 'four', count: 4 });
  });

  test('Top10Printer prints output', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    Top10Printer.print([{ word: 'foo', count: 3 }]);
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });

  test('WordCount.main executes without error', () => {
    // Patch FileReader to use our file
    expect(() => WordCount.main(WORDS_FILE)).not.toThrow();
  });
});