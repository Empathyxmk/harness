const tree = require('../../parser/tree');

describe('Tree module (public)', () => {
  it('should export a function or object (public)', () => {
    expect(['function', 'object']).toContain(typeof tree);
  });

  it('should handle a different tree node (public)', () => {
    // Try to create/describe a node with different data than existing tests
    if (typeof tree.createNode === 'function') {
      const node = tree.createNode('customType', 18);
      expect(node.type).toBe('customType');
      expect(node.value).toBe(18);
    }
  });
});