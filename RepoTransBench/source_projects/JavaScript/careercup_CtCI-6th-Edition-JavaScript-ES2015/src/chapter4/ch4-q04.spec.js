import { expect } from 'chai';
import { isBalanced } from './ch4-q04';

// Minimal Tree node/Tree definition for testing (to simulate input)
class Node {
    constructor(val) {
        this.val = val;
        this.left = this.right = null;
    }
}

class Tree {
    constructor() {
        this.root = null;
    }
    add(val) {
        if (!this.root) {
            this.root = new Node(val);
            return;
        }
        let node = this.root;
        while (true) {
            if (val < node.val) {
                if (!node.left) { node.left = new Node(val); return; }
                node = node.left;
            } else {
                if (!node.right) { node.right = new Node(val); return; }
                node = node.right;
            }
        }
    }
}

// Actually test the isBalanced function
describe('isBalanced', () => {

    it('returns true for empty or undefined tree', () => {
        expect(isBalanced(null)).to.equal(true);
        expect(isBalanced(undefined)).to.equal(true);
        expect(isBalanced({})).to.equal(true);
        expect(isBalanced({root:null})).to.equal(true);
    });

    it('returns true for single node', () => {
        const tree = new Tree();
        tree.add(12);
        expect(isBalanced(tree)).to.equal(true);
    });

    it('returns true for small balanced tree', () => {
        const tree = new Tree();
        [10,5,15].forEach(v => tree.add(v));
        expect(isBalanced(tree)).to.equal(true);
    });

    it('returns true for larger fully balanced tree', () => {
        // Create a complete binary tree to depth 3
        const tree = new Tree();
        [8,4,12,2,6,10,14,1,3,5,7,9,11,13,15].forEach(v => tree.add(v));
        expect(isBalanced(tree)).to.equal(true);
    });

    it('returns false for tree with path difference > 1', () => {
        // Create an unbalanced tree
        const tree = new Tree();
        [10,5,15,1,7,12,18,9,8].forEach(v => tree.add(v));
        // Manually make 1's left child a deep branch:
        tree.root.left.left.left = new Node(0);
        tree.root.left.left.left.left = new Node(-1);
        expect(isBalanced(tree)).to.equal(false);
    });

    it('returns true for skewed tree with depth diff = 1', () => {
        const tree = new Tree();
        tree.add(10);
        tree.add(20);
        expect(isBalanced(tree)).to.equal(true); // left empty, right 1 deep: difference 1
    });

    it('returns false for a chain of 4 nodes (skewed)', () => {
        const tree = new Tree();
        [1,2,3,4].forEach(v => tree.add(v));
        expect(isBalanced(tree)).to.equal(false); // depths: min=1, max=4
    });

    it('returns true if depth min and max are exactly one apart', () => {
        const tree = new Tree();
        [2, 1, 3].forEach(v => tree.add(v));
        expect(isBalanced(tree)).to.equal(true);
    });

    it('returns false for tree where leaves are at 2 and 4 deep', () => {
        const tree = new Tree();
        //       5
        //     /   \
        //    2     10
        //   /       \
        //  1         20
        //            /
        //           15
        [5,2,10,1,20,15].forEach(v => tree.add(v));
        expect(isBalanced(tree)).to.equal(false);
    });

});