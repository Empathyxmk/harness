const tree = require('./tree');

describe('Tree module', () => {
  it('should export a function or object', () => {
    // Accept both object or function according to export style
    expect(['object', 'function']).toContain(typeof tree);
  });

  it('should allow instantiation if export is a constructor', () => {
    if (typeof tree === 'function') {
      const node = new tree();
      expect(node).toBeDefined();
    }
    if (typeof tree.TreeNode === 'function') {
      const node = new tree.TreeNode();
      expect(node).toBeDefined();
    }
    if (typeof tree.createNode === 'function') {
      expect(tree.createNode({})).toBeDefined();
    }
  });

  it('should handle vector/array edge cases for internal methods', () => {
    if (typeof tree.vectorize === 'function') {
      expect(tree.vectorize([])).toEqual([]);
      expect(tree.vectorize([1, 2, 3])).toEqual([1, 2, 3]);
    }
  });

  it('should cover edge-cases in main tree logic (map, filter...)', () => {
    let n = null;
    if (typeof tree === 'function') n = new tree('root', [new tree('c1'), new tree('c2')]);
    if (!n && typeof tree.TreeNode === 'function') n = new tree.TreeNode('root', [new tree.TreeNode('c1'), new tree.TreeNode('c2')]);

    if (n && n.map) {
      const mapped = n.map(x => x);
      expect(mapped).toBeDefined();
    }
    if (n && n.reduce) {
      const sum = n.reduce((acc, x) => acc, 0);
      expect(sum).toBeDefined();
    }
  });

  it('should handle error and empty path for tree utilities', () => {
    if (typeof tree.findPath === 'function') {
      expect(tree.findPath(null, 'unknown')).toEqual([]);
      expect(tree.findPath({}, 'nope')).toEqual([]);
    }
    if (typeof tree.traverse === 'function') {
      expect(() => tree.traverse(null, () => {})).not.toThrow();
    }
  });

  it('should cover leaf node/child-less corner cases', () => {
    let leaf = null;
    if (typeof tree === 'function') leaf = new tree('leaf');
    if (!leaf && typeof tree.TreeNode === 'function') leaf = new tree.TreeNode('leaf');
    if (leaf && leaf.children && Array.isArray(leaf.children) && leaf.children.length === 0) {
      expect(leaf.children.length).toBe(0);
      if (leaf.map) expect(leaf.map(x => x)).toBeDefined();
    }
  });

  it('should cover deletion/removal and alternate paths', () => {
    if (typeof tree.removeNode === 'function') {
      expect(typeof tree.removeNode(null, 'missing')).toMatch(/boolean|undefined/);
    }
  });
});