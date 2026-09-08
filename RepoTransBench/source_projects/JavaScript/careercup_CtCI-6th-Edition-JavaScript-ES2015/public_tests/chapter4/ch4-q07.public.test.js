import { expect } from 'chai';
import * as funcs from '../../src/chapter4/ch4-q07';

for (let key in funcs) {
  let func = funcs[key];

  describe('PUBLIC ch4-q07: ' + key, function() {

    it('returns project where there is only one project (public)', function() {
      expect(func([2], [])).to.eql([2]);
    });

    it('returns projects in the reverse of supplied order with no dependencies (public)', function() {
      expect(func([3, 8, 1, 4], [])).to.eql([4, 1, 8, 3]);
    });

    it('returns in the right order with simple chain of dependencies (public)', function() {
      expect(func([7, 2, 6, 5], [
        [5, 6],
        [6, 2],
        [2, 7]
      ])).to.eql([7, 2, 6, 5]);
    });

    it('throws an error when dependences are cyclic (public)', function() {
      expect(() => func([5, 8, 3, 2], [
        [2, 5],
        [5, 8],
        [8, 3],
        [3, 5]
      ])).to.throw('dependencies are cyclic');
    });

    it('correctly orders with larger acyclic graph (public)', function() {
      expect(func([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [
        [12, 11],
        [13, 11],
        [14, 12],
        [16, 12],
        [15, 13],
        [17, 13],
        [18, 14],
        [21, 18],
        [22, 18],
        [20, 16],
        [20, 15],
        [19, 17],
        [23, 20],
        [23, 19],
        [24, 23]
      ])).to.eql([25, 11, 13, 17, 19, 15, 12, 16, 20, 23, 24, 14, 18, 22, 21]);
    });

  });

}