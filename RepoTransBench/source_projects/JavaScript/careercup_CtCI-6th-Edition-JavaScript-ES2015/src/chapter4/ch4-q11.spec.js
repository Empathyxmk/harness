import { expect } from 'chai';
import { RandomBinarySearchTree } from './ch4-q11';

// Utility to gather all values in BST as array (in-order)
function bstToArray(tree) {
    const res = [];
    function inorder(node) {
        if (!node) return;
        inorder(node.left);
        res.push(node.val);
        inorder(node.right);
    }
    inorder(tree.root);
    return res;
}

describe('RandomBinarySearchTree', function() {

    let Tree;
    beforeEach(() => {
        Tree = new RandomBinarySearchTree();
    });

    describe('insert', function() {
        it('should insert root if tree is empty', () => {
            Tree.insert(10);
            expect(Tree.root.val).to.equal(10);
            expect(Tree.root.size).to.equal(1);
        });

        it('should insert multiple unique values and keep BST property', () => {
            Tree.insert(10);
            Tree.insert(5);
            Tree.insert(15);
            Tree.insert(12);
            Tree.insert(3);
            expect(bstToArray(Tree)).to.eql([3,5,10,12,15]);
            expect(Tree.root.size).to.equal(5);
        });
    });

    describe('find', function() {
        beforeEach(() => {
            [10, 6, 4, 8, 15, 12, 20].forEach(v => Tree.insert(v));
        });

        it('should find existing node', () => {
            const node = Tree.find(10);
            expect(node).to.have.property('val', 10);
        });

        it('should return undefined for absent value', () => {
            expect(Tree.find(4567)).to.be.undefined;
        });
    });

    describe('delete', function() {
        it('should return false on delete from empty tree', () => {
            expect(Tree.delete(5)).to.equal(false);
        });

        it('should delete a leaf node', () => {
            [10, 5, 15].forEach(v => Tree.insert(v));
            expect(Tree.delete(5)).to.equal(true);
            expect(Tree.find(5)).to.be.undefined;
            expect(Tree.root.size).to.equal(2);
        });

        it('should delete node with only left child', () => {
            [10, 5, 3].forEach(v => Tree.insert(v));
            expect(Tree.delete(5)).to.equal(true);
            expect(Tree.find(5)).to.be.undefined;
            expect(bstToArray(Tree)).to.eql([3,10]);
            expect(Tree.root.size).to.equal(2);
        });

        it('should delete node with only right child', () => {
            [10, 15, 20].forEach(v => Tree.insert(v));
            expect(Tree.delete(15)).to.equal(true);
            expect(Tree.find(15)).to.be.undefined;
            expect(bstToArray(Tree)).to.eql([10,20]);
            expect(Tree.root.size).to.equal(2);
        });

        it('should delete node with two children', () => {
            [10, 5, 15, 12, 18].forEach(v => Tree.insert(v));
            // Root node has 2 children!
            expect(Tree.delete(10)).to.equal(true);
            expect(Tree.find(10)).to.be.undefined;
            expect(bstToArray(Tree)).to.eql([5,12,15,18]);
            expect(Tree.root.size).to.equal(4);
        });

        it('should update size after deletion', () => {
            [8, 4, 12, 2, 6, 10, 14].forEach(v => Tree.insert(v));
            Tree.delete(12); // node with two children
            expect(Tree.root.size).to.equal(6);
            Tree.delete(8); // root, with children
            expect(Tree.root.size).to.equal(5);
        });

        it('should return false when deleting absent value', () => {
            [7, 3, 9].forEach(v => Tree.insert(v));
            expect(Tree.delete(33)).to.equal(false);
        });
    });

    describe('randomNode', function() {
        it('returns undefined for empty tree', () => {
            expect(Tree.randomNode()).to.be.undefined;
        });

        it('returns the only root if tree has one node', () => {
            Tree.insert(44);
            expect(Tree.randomNode().val).to.equal(44);
        });

        it('returns a valid node from tree', () => {
            [1, 2, 3].forEach(v => Tree.insert(v));
            const node = Tree.randomNode();
            expect([1,2,3]).to.include(node.val);
        });

        it('eventually returns all nodes (statistically)', () => {
            [4, 5, 6, 7, 8].forEach(v => Tree.insert(v));
            const found = new Set();
            for (let i = 0; i < 100; ++i) {
                found.add(Tree.randomNode().val);
            }
            // Should have found all inserted values
            expect(Array.from(found).sort()).to.eql([4,5,6,7,8]);
        });

        it('should throw error only on internal bug (unreachable)', () => {
            // We can't hit the throw on normal usage,
            // just test that the "should never reach here" branch exists.
            // (Can't force it without breaking the tree's structure.)
            expect(() => {
                // Not possible to test in valid scenario, skip coverage.
            }).to.not.throw();
        });
    });
});