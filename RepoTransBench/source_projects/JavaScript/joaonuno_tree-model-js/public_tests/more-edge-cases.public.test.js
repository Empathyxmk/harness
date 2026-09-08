const chai = require('chai');
const assert = chai.assert;
const TreeModel = require('..');

describe('TreeModel extra PUBLIC edge cases', function () {
    let treeModel;
    beforeEach(() => {
        treeModel = new TreeModel();
    });

    it('Node.getIndex should return 0 if called on root (isRoot true, different id)', function () {
        const root = treeModel.parse({ id: 'z' });
        assert.equal(root.getIndex(), 0);
    });

    it('Node.getIndex should find index of child with other values', function () {
        const root = treeModel.parse({ id: 3, children: [{ id: 4 }] });
        assert.equal(root.children[0].getIndex(), 0);
    });

    it('Node.getPath should build correct path for another deep child', function () {
        const root = treeModel.parse({
            id: 5,
            children: [
                { id: 6, children: [{ id: 7 }] },
            ]
        });
        const child = root.children[0].children[0];
        const path = child.getPath();
        assert.deepEqual(path.map(n => n.model.id), [5, 6, 7]);
    });

    it('addChild should fill empty childrenPropertyName if not array, different ids', function () {
        const root = treeModel.parse({ id: 10 });
        root.model.children = undefined;
        root.addChild(treeModel.parse({ id: 20 }));
        assert.equal(root.children.length, 1);
        assert.deepEqual(root.model.children[0], { id: 20 });
    });

    it('addChildAtIndex should throw if invalid index (<0) for public', function () {
        const root = treeModel.parse({ id: 100 });
        const child = treeModel.parse({ id: 101 });
        assert.throws(
            () => root.addChildAtIndex(child, -2),
            /Invalid index/
        );
    });

    it('addChildAtIndex should throw if invalid index (>children.length) for public', function () {
        const root = treeModel.parse({ id: 21, children: [{ id: 22 }] });
        const child = treeModel.parse({ id: 23 });
        assert.throws(
            () => root.addChildAtIndex(child, 3),
            /Invalid index/
        );
    });

    it('setIndex should throw if index < 0 (public)', function () {
        const root = treeModel.parse({ id: 99, children: [{ id: 98 }, { id: 97 }] });
        assert.throws(
            () => root.children[0].setIndex(-7),
            /Invalid index/
        );
    });

    it('setIndex should throw if index >= children.length (public)', function () {
        const root = treeModel.parse({ id: 83, children: [{ id: 84 }, { id: 85 }] });
        assert.throws(
            () => root.children[0].setIndex(2),
            /Invalid index/
        );
    });

    it('setIndex should allow moving position within allowed range (public)', function () {
        const root = treeModel.parse({ id: 50, children: [{ id: 51 }, { id: 52 }, { id: 53 }] });
        root.children[1].setIndex(0); // move child 52 from index 1 to 0
        assert.equal(root.children[0].model.id, 52);
        assert.deepEqual(
            root.model.children.map(c => c.id),
            [52,51,53]
        );
    });

    it('setIndex should throw if called on root node and index != 0 (public)', function () {
        const root = treeModel.parse({ id: 75, children: [{ id: 76 }] });
        assert.throws(
            () => root.setIndex(5),
            /Invalid index/
        );
    });

    it('setIndex should return self if called on root node and index==0 (public)', function () {
        const root = treeModel.parse({ id: 60, children: [{ id: 61 }] });
        const res = root.setIndex(0);
        assert.equal(res, root);
    });
});