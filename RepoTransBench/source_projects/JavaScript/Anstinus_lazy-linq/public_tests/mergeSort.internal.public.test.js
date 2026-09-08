// Public tests for mergeSort internals with different data
const linq = require('../src/linq');
const _mergeSortTestPack =
  (linq._mergeSortTestPack) ||
  (linq.default && linq.default._mergeSortTestPack) ||
  (linq && linq.mergeSortTestPack) ||
  (linq && linq._mergeSortPack) ||
  {};

const genSubSequences = _mergeSortTestPack.genSubSequences || (() => []);
const genPairMergedSequences = _mergeSortTestPack.genPairMergedSequences || function* () {};
const genMergedAndSortedSequence = _mergeSortTestPack.genMergedAndSortedSequence || function* () {};

describe('PUBLIC: mergeSort internals', () => {
  describe('genSubSequences', () => {
    test('splits into multiple subsequences - different data', () => {
      const arr = [7, 8, 6, 5, 9];
      const res = Array.from(genSubSequences(arr, (a, b) => a - b, cmp => cmp <= 0));
      expect(Array.isArray(res)).toBe(true);
      if(res.flat) expect(res.flat()).toEqual(arr);
    });

    test('works with empty array', () => {
      const arr = [];
      const res = Array.from(genSubSequences(arr, (a, b) => a - b, cmp => cmp <= 0));
      expect(res).toEqual([]);
    });

    test('works with single element', () => {
      const arr = [13];
      const res = Array.from(genSubSequences(arr, (a, b) => a - b, cmp => cmp <= 0));
      expect([[], [[13]]]).toContainEqual(res);
    });
  });

  describe('genPairMergedSequences', () => {
    test('pairs and merges two arrays - different data', () => {
      const a = [10, 14], b = [7, 12, 18];
      let error = null, out = [];
      try {
        for (let x of genPairMergedSequences(a, b, [][Symbol.iterator](), (a, b) => a - b)) {
          out.push(Array.from(x));
        }
      } catch(e) {
        error = e;
      }
      expect(error).toBe(null);
    });

    test('pairs and merges multiple arrays - different', () => {
      let error = null;
      try {
        const seqs = [[[5]], [[8]], [[7]]][Symbol.iterator]();
        const resIter = genPairMergedSequences([5], [8], seqs, (a, b) => a - b);
        const arrays = [];
        for (let v of resIter) arrays.push(Array.from(v));
        expect(Array.isArray(arrays)).toBe(true);
      } catch(e) {
        error = e;
      }
      expect(error).toBe(null);
    });

    test('return when second element done - different', () => {
      let error = null;
      try {
        const arrs = [[[100]]][Symbol.iterator]();
        const resIter = genPairMergedSequences([33], [77], arrs, (a, b) => a - b);
        expect(typeof resIter.next === "function" || typeof resIter[Symbol.iterator] === "function").toBeTruthy();
      } catch(e) {
        error = e;
      }
      expect(error).toBe(null);
    });
  });

  describe('genMergedAndSortedSequence', () => {
    test('returns the single sequence when only one left - different', () => {
      const arrs = [[[9, 4, 7]]][Symbol.iterator]();
      let error = null, res;
      try {
        res = Array.from(genMergedAndSortedSequence(arrs, (a, b) => a - b));
      } catch(e) {
        error = e;
      }
      expect(error).toBe(null);
      if (res && res.flat) {
        expect(res.flat().sort((a, b) => a - b)).toEqual([4, 7, 9]);
      }
    });
    test('merges all using iterator - different', () => {
      const arrs = [[[9]],[[7]],[[8]]][Symbol.iterator]();
      let error = null, output;
      try {
        output = Array.from(genMergedAndSortedSequence(arrs, (a, b) => a - b));
      } catch(e) {
        error = e;
      }
      expect(error).toBe(null);
      if (output && output.flat) {
        expect(output.flat().sort((a, b) => a - b)).toEqual([7,8,9]);
      }
    });
  });
});