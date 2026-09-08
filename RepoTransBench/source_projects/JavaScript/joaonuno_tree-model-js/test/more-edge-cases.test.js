const chai = require('chai');
const assert = chai.assert;
const TreeModel = require('..');

describe('TreeModel extra edge cases', function () {
    let treeModel;
    beforeEach(() => {
        treeModel = new TreeModel();
    });

    it('Node.getIndex should return 0 if called on root (isRoot true)', function () {
        const root = treeModel.parse({ id: 'a' });
        assert.equal(root.getIndex(), 0);
    });

    it('Node.getIndex should find index of child', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }] });
        assert.equal(root.children[0].getIndex(), 0);
    });

    it('Node.getPath should build correct path for deep child', function () {
        const root = treeModel.parse({
            id: 0,
            children: [
                { id: 1, children: [{ id: 2 }] },
            ]
        });
        const child = root.children[0].children[0];
        const path = child.getPath();
        assert.deepEqual(path.map(n => n.model.id), [0, 1, 2]);
    });

    // Removed (invalid) test for children: 5 since README specifies children must be array or omitted
    // and original implementation does not throw for this scenario

    it('addChild should fill empty childrenPropertyName if not array', function () {
        const root = treeModel.parse({ id: 1 });
        root.model.children = undefined;
        // Should set children property to [] before pushing
        root.addChild(treeModel.parse({ id: 2 }));
        assert.equal(root.children.length, 1);
        assert.deepEqual(root.model.children[0], { id: 2 });
    });

    it('addChildAtIndex should throw if invalid index (<0)', function () {
        const root = treeModel.parse({ id: 1 });
        const child = treeModel.parse({ id: 2 });
        assert.throws(
            () => root.addChildAtIndex(child, -1),
            /Invalid index/
        );
    });

    it('addChildAtIndex should throw if invalid index (>children.length)', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }] });
        const child = treeModel.parse({ id: 3 });
        assert.throws(
            () => root.addChildAtIndex(child, 2),
            /Invalid index/
        );
    });

    it('setIndex should throw if index < 0', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }, { id: 3 }] });
        assert.throws(
            () => root.children[0].setIndex(-1),
            /Invalid index/
        );
    });

    it('setIndex should throw if index >= children.length', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }, { id: 3 }] });
        assert.throws(
            () => root.children[0].setIndex(2),
            /Invalid index/
        );
    });

    it('setIndex should allow moving position within allowed range', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }, { id: 3 }, { id: 4 }] });
        // Move child 2 from index 0 to 1
        root.children[0].setIndex(1);
        assert.equal(root.children[1].model.id, 2);
        assert.deepEqual(
            root.model.children.map(c => c.id),
            [3,2,4]
        );
    });

    it('setIndex should throw if called on root node and index != 0', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }] });
        assert.throws(
            () => root.setIndex(1),
            /Invalid index/
        );
    });

    it('setIndex should return self if called on root node and index==0', function () {
        const root = treeModel.parse({ id: 1, children: [{ id: 2 }] });
        const res = root.setIndex(0);
        assert.equal(res, root);
    });
});