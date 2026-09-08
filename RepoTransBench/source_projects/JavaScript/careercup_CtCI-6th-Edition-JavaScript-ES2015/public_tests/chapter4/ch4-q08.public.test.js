import { expect } from 'chai';
import { Tree } from '../../src/chapter4/helpers';
import * as funcs from '../../src/chapter4/ch4-q08';

for (let key in funcs) {
  let func = funcs[key];

  describe('PUBLIC ch4-q08: ' + key, function() {

    beforeEach(function() {
      this.tree = new Tree();
    });

    it('throws an error if either node is null (public)', function() {
      this.tree.add(17);
      expect(() => func(null, null)).to.throw('node1 and node2 must both be valid nodes');
      expect(() => func(this.tree.root, null)).to.throw('node1 and node2 must both be valid nodes');
      expect(() => func(null, this.tree.root)).to.throw('node1 and node2 must both be valid nodes');
    });

    it('returns right value for simple 3 node balanced tree (public)', function() {
      [20, 15, 25].forEach(v => this.tree.add(v));
      expect(func(this.tree.root.left, this.tree.root.right)).to.equal(20);
      expect(func(this.tree.root, this.tree.root.right)).to.equal(20);
      expect(func(this.tree.root.left, this.tree.root)).to.equal(20);
    });

    it('returns correct values for larger balanced tree (public)', function() {
      [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30].forEach(v => this.tree.add(v));

      expect(func(this.tree.root.left.left.left, this.tree.root.left.left.left)).to.equal(2);
      expect(func(this.tree.root.left.left.left, this.tree.root.left.left.right)).to.equal(4);
      expect(func(this.tree.root.left.left.right, this.tree.root.left.left.left)).to.equal(4);

      expect(func(this.tree.root.left, this.tree.root.left)).to.equal(8);
      expect(func(this.tree.root.left.left.right, this.tree.root.left)).to.equal(8);
      expect(func(this.tree.root.left.left.right, this.tree.root.left.right)).to.equal(8);
      expect(func(this.tree.root.left.left.left, this.tree.root.left.right.left)).to.equal(8);
      expect(func(this.tree.root.left.left.left, this.tree.root.left.right.right)).to.equal(8);
      expect(func(this.tree.root.left.left.right, this.tree.root.left.right.left)).to.equal(8);
      expect(func(this.tree.root.left.left.right, this.tree.root.left.right.right)).to.equal(8);

      expect(func(this.tree.root.left.left.right, this.tree.root)).to.equal(16);
      expect(func(this.tree.root.left.left.right, this.tree.root.right)).to.equal(16);
      expect(func(this.tree.root.left.left.right, this.tree.root.right.right)).to.equal(16);
      expect(func(this.tree.root.left.left.right, this.tree.root.right.left.left)).to.equal(16);
      expect(func(this.tree.root.left.left.right, this.tree.root.right.left.right)).to.equal(16);
      expect(func(this.tree.root.left.left.right, this.tree.root.right.right.left)).to.equal(16);
      expect(func(this.tree.root.left.left.right, this.tree.root.right.right.right)).to.equal(16);
    });

  });

}