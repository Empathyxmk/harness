import {
  _mergeSortTestPack as algo
}
from '../src/linq';

function iterToArray(iter) {
  let elem;
  let result = [];
  while (!(elem = iter.next()).done) {
    result.push(elem.value);
  }
  return result;
}

describe('PUBLIC: sort algo -> ', function () {
  describe('genSubSequences()', function () {

    it('should divided sequence by natural order - different data', function () {
      let data = [9, 8, 10, 13, 7, 5, 4, 11, 8, 10];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => x - y, x => x <= 0));
      expect(result).toEqual([
        [9],
        [8, 10, 13],
        [7],
        [5, 4, 11],
        [8, 10],
      ]);
    });

    it('should divide according to @comp - different data', function () {
      let data = [11, 10, 14, 18, 15, 11, 12, 14, 12, 16];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => y - x, x => x <= 0));
      expect(result).toEqual([
        [11, 10],
        [14],
        [18, 15, 11, 12],
        [14, 12],
        [16]
      ]);
    });

    it('should divide according to @compGroupChecker - different data', function () {
      let data = [10, 10, 11, 13, 13, 14, 15, 15, 16, 17];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => x - y, x => x === 0));
      expect(result).toEqual([
        [10, 10],
        [11],
        [13, 13],
        [14],
        [15,15],
        [16],
        [17]
      ]);
    });

    it('when sequence is empty, should return empty sequence', function () {
      let data = [];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => x - y, x => x <= 0));
      expect(result.length).toBe(0);
    });

    it('should divide undefined separately - different', function () {
      let data = [18, 17, 15, undefined, 20, 12, 13, 10];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => x - y, x => x <= 0));
      expect(result).toEqual([
        [18],
        [17, 15],
        [undefined],
        [20],
        [12, 13],
        [10]
      ]);
    });

    it('should divide multiple undefined separately - different', function () {
      let data = [9, undefined, undefined, 5, 4, 6];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => x - y, x => x <= 0));
      expect(result).toEqual([
        [9],
        [undefined],
        [undefined],
        [5],
        [4,6]
      ]);
    });

    it('should divide invalid value separately - different', function () {
      let data = [10, null, 'xyz', 3, 6];
      let result = iterToArray(algo.genSubSequences(data, (x, y) => x - y, x => x <= 0));
      expect(result).toEqual([
        [10],
        [null],
        ['xyz'],
        [3,6]
      ]);
    });
  });

  describe('genTwoMergedSequence()', function () {
    it('should merge - different data', function () {
      let data1 = [5, 12, 15];
      let data2 = [7, 13, 17];
      let result = iterToArray(algo.genTwoMergedSequence(data1, data2, (x, y) => x - y));
      expect(result).toEqual([5, 7, 12, 13, 15, 17]);
    });

    it('should merge according to @comp - different data', function () {
      let data1 = [15, 12, 5];
      let data2 = [19, 15, 10];
      let result = iterToArray(algo.genTwoMergedSequence(data1, data2, (x, y) => y - x));
      expect(result).toEqual([19, 15, 15, 12, 10, 5]);
    });

    it('should work fine when one sequence is empty - different', function () {
      let data1 = [8, 14];
      let data2 = [6, 9, 20];

      var result = iterToArray(algo.genTwoMergedSequence([], data2, (x, y) => x - y));
      expect(result).toEqual([6, 9, 20]);

      var result2 = iterToArray(algo.genTwoMergedSequence(data1, [], (x, y) => x - y));
      expect(result2).toEqual([8, 14]);
    });

    it('should merge undefined alone - different', function () {
      let data1 = [20, 25];
      let data2 = [undefined];
      let result = iterToArray(algo.genTwoMergedSequence(data1, data2, (x, y) => x - y));
      expect(result).toEqual([undefined, 20, 25]);
    });

    it('should merge undefined mixed - different', function () {
      let data1 = [13, 15, undefined];
      let data2 = [9, 20];
      let result = iterToArray(algo.genTwoMergedSequence(data1, data2, (x, y) => x - y));
      expect(result).toEqual([9, 13, 15, 20, undefined]);
    });

    it('should merge undefined mixed in middle - different', function () {
      let data1 = [5, undefined, 12];
      let data2 = [1, 9];
      let result = iterToArray(algo.genTwoMergedSequence(data1, data2, (x, y) => x - y));
      expect(result).toEqual([1, 5, 9, 12, undefined]);
    });
  });
});