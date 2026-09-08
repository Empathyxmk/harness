const nodeCreator = require('../src/nodeCreator');

describe('nodeCreator extra branch/edge coverage', function() {
    it('should reject unhandled type', function() {
        expect(() => nodeCreator.createNode(true, {}, () => {}, null)).toThrow();
    });

    it('should return false for isFrozen non-object', function() {
        expect(nodeCreator.isFrozen(123)).toBe(false);
        expect(nodeCreator.isFrozen(null)).toBe(false);
    });

    it('should set value and call updateCB', function() {
        let updated = false;
        const node = nodeCreator.createNode([], {}, () => {updated = true; return [42];}, "freezer");
        node.set(0, 100);
        expect(updated).toBe(true);
    });

    it('should delete using node delete', function() {
        let updated = false;
        const node = nodeCreator.createNode([], {}, () => {updated = true; return [];}, "freezer");
        node.push(1);
        node.push(2);
        node['delete'](0); // coverage for 'delete' as non-function property
        expect(updated).toBe(true);
    });
});