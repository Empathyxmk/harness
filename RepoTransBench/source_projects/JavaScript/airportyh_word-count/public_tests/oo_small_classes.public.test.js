const fs = require('fs');
const path = require('path');

const WORDS_FILE = path.join(__dirname, 'test_words2_public.txt');
// Different input for public tests, new word and different frequency pattern
const WORDS_TEXT = 'dog cat cat, mouse. mouse mouse. rabbit rabbit rabbit rabbit';

beforeAll(() => {
  fs.writeFileSync(WORDS_FILE, WORDS_TEXT, 'utf8');
});

afterAll(() => {
  fs.unlinkSync(WORDS_FILE);
});

describe('4.oo-small-classes.js classes (public)', () => {
  const { Tokenizer, FileReader, Tally, Top10Printer, WordCount } = require('../4.oo-small-classes.js.tmp.js');

  test('Tokenizer splits correctly (public)', () => {
    const t = new Tokenizer();
    expect(t.tokenize('red green,blue')).toEqual(['red', 'green', 'blue']);
  });

  test('FileReader reads text and words (public)', () => {
    const fr = new FileReader(WORDS_FILE);
    expect(fr.read()).toBe(WORDS_TEXT);
    expect(fr.readWords()).toContain('mouse');
  });

  test('Tally tallies, sorts, slices correctly (public)', () => {
    const fr = new FileReader(WORDS_FILE);
    const tally = new Tally(fr.readWords());
    expect(tally.tally['mouse']).toBe(3);
    expect(tally.tally['rabbit']).toBe(4);
    expect(tally.getTop10()[0]).toEqual({ word: 'rabbit', count: 4 });
  });

  test('Top10Printer prints output (public)', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    Top10Printer.print([{ word: 'bar', count: 6 }]);
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });

  test('WordCount.main executes without error (public)', () => {
    // Patch FileReader to use our file
    expect(() => WordCount.main(WORDS_FILE)).not.toThrow();
  });
});