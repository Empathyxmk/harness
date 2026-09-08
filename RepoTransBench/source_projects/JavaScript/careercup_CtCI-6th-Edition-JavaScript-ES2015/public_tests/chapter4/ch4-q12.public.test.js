import { expect } from 'chai';
import { Tree } from '../../src/chapter4/helpers';
import * as funcs from '../../src/chapter4/ch4-q12';

// In previous attempts, paths were non-unique due to BST structure. 
// For unique-path-sum, ensure no overlapping paths with same sum.

for (let key in funcs) {
  let func = funcs[key];

  describe('PUBLIC ch4-q12: ' + key, function() {
    let tree;

    beforeEach(function() {
      tree = new Tree();
    });

    it('throws on empty tree (public)', function() {
      expect(() => func(tree, 1)).to.throw(/tree must be valid/);
    });

    it('returns 1 for root only, matching value (public)', function() {
      tree.add(51);
      expect(func(tree, 51)).to.equal(1);
      expect(func(tree, 11)).to.equal(0);
    });

    it('returns correct counts with balanced tree (public)', function() {
      // Tree:
      //        20
      //       /  \
      //     10    35
      //    /  \     \
      //   5   15     45
      //         \
      //         16
      [20, 10, 35, 5, 15, 16, 45].forEach(v => tree.add(v));
      // Path for 16: only from 16 node itself
      expect(func(tree, 16)).to.equal(1); // 16 only
      // Path: 10 -> 15 -> 16 = 41
      expect(func(tree, 10+15+16)).to.equal(1); // 10->15->16
      // Path: 35->45 = 80
      expect(func(tree, 35+45)).to.equal(1); // 35->45
      // Path: 20->10 = 30
      expect(func(tree, 20+10)).to.equal(1); // 20->10
    });

    it('returns correct counts with unbalanced tree (public)', function() {
      //           90
      //          /
      //        40
      //       /
      //     18
      //    /
      //   8
      [90, 40, 18, 8].forEach(v => tree.add(v));
      expect(func(tree, 8)).to.equal(1); // 8 only
      expect(func(tree, 40+18+8)).to.equal(1); // 40->18->8
      expect(func(tree, 90+40)).to.equal(1); // 90->40
    });

    it('returns correct counts with paths that equal value (public)', function() {
      //          100
      //         /   \
      //      53     140
      //         \
      //         67
      //           \
      //           88
      [100, 53, 140, 67, 88].forEach(v => tree.add(v));
      expect(func(tree, 140)).to.equal(1); // 140 only
      expect(func(tree, 53+67+88)).to.equal(1); // 53->67->88
      expect(func(tree, 100+53)).to.equal(1); // 100->53
    });
  });
}