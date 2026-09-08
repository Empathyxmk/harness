const Trie = require('../../lib/dataStructures/trie');

const word1 = 'Winterfell';
const word2 = 'Winter';
const fruit1 = 'kiwi';
const fruit2 = 'melon';
const fruit3 = 'peach';

describe('Given a trie (public test)', () => {
  let tree;

  describe('containing the word "Winterfell"', () => {
    beforeEach(() => {
      tree = new Trie();
      tree.add(word1);
    });

    it('the tree`s head should only contain one entry', () => {
      expect(Object.keys(tree.head).length).toBe(1);
    });

    it('the tree`s head should contain the property W.', () => {
      expect(tree.head.W).toBeDefined();
    });

    it('the hasWord() method should be able to find Winterfell', () => {
      expect(tree.hasWord(word1)).toBe(true);
    });
  });

  describe('containing the words "Winterfell" and "Winter"', () => {
    beforeEach(() => {
      tree = new Trie();
      tree.add(word1);
      tree.add(word2);
    });

    afterEach(() => {
      tree = null;
    });

    it('the tree`s head should only contain one entry', () => {
      expect(Object.keys(tree.head).length).toBe(1);
    });

    it('the tree`s head should contain the property W.', () => {
      expect(tree.head.W).toBeDefined();
    });

    it(`the hasWord() method should be able to find ${word1}`, () => {
      expect(tree.hasWord(word1)).toBe(true);
    });

    it(`the hasWord() method should be able to find ${word2}`, () => {
      expect(tree.hasWord(word2)).toBe(true);
    });
  });

  describe('containing the words "blue", "blues", "bluest", and "blueberry"', () => {
    const t1 = 'blue';
    const t2 = 'blues';
    const t3 = 'blueberry';
    const t4 = 'bluest';

    beforeEach(() => {
      tree = new Trie();
      tree.add(t1);
      tree.add(t2);
      tree.add(t3);
      tree.add(t4);
    });

    afterEach(() => {
      tree = null;
    });

    it('the tree`s head should contain one entry', () => {
      expect(Object.keys(tree.head).length).toBe(1);
    });

    it('the tree`s head should contain the property b.', () => {
      expect(tree.head.b).toBeDefined();
    });

    it(`the hasWord() method should be able to find ${t1}`, () => {
      expect(tree.hasWord(t1)).toBe(true);
    });

    it(`the hasWord() method should be able to find ${t2}`, () => {
      expect(tree.hasWord(t2)).toBe(true);
    });

    it(`the hasWord() method should be able to find ${t3}`, () => {
      expect(tree.hasWord(t3)).toBe(true);
    });

    it(`the hasWord() method should be able to find ${t4}`, () => {
      expect(tree.hasWord(t4)).toBe(true);
    });
  });

  describe('containing the words "kiwi", "melon", and "peach"', () => {
    beforeEach(() => {
      tree = new Trie();
      tree.add(fruit1);
      tree.add(fruit2);
      tree.add(fruit3);
    });

    afterEach(() => {
      tree = null;
    });

    it('the tree`s head should contain three entries', () => {
      expect(Object.keys(tree.head).length).toBe(3);
    });

    it('the tree`s head should contain the property k.', () => {
      expect(tree.head.k).toBeDefined();
    });

    it('the tree`s head should contain the property m.', () => {
      expect(tree.head.m).toBeDefined();
    });

    it('the tree`s head should contain the property p.', () => {
      expect(tree.head.p).toBeDefined();
    });

    it(`the hasWord() method should be able to find ${fruit1}`, () => {
      expect(tree.hasWord(fruit1)).toBe(true);
    });

    it(`the hasWord() method should be able to find ${fruit2}`, () => {
      expect(tree.hasWord(fruit2)).toBe(true);
    });

    it(`the hasWord() method should be able to find ${fruit3}`, () => {
      expect(tree.hasWord(fruit3)).toBe(true);
    });
  });

  describe('where you add(undefined)', () => {
    beforeEach(() => {
      tree = new Trie();
    });

    it('the add() method will throw an exception', () => {
      expect(tree.add).toThrow();
    });
  });

  describe('where you add a valid word, but an undefined or null value', () => {
    beforeEach(() => {
      tree = new Trie();
    });

    it('the add() method will throw an exception', () => {
      expect(() => tree.add('bar', undefined)).toThrow();
    });
  });
});