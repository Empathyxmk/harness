const maxDepth = require('./maximum-depth-of-binary-tree');

function TreeNode(val) {
  this.val = val;
  this.left = this.right = null;
}

describe('maxDepth', () => {
  test('null root returns 0', () => {
    expect(maxDepth(null)).toBe(0);
  });

  test('single node', () => {
    const root = new TreeNode(1);
    expect(maxDepth(root)).toBe(1);
  });

  test('tree with two levels', () => {
    const root = new TreeNode(1);
    root.left = new TreeNode(2);
    expect(maxDepth(root)).toBe(2);
  });

  test('left-skewed tree', () => {
    const root = new TreeNode(1);
    root.left = new TreeNode(2);
    root.left.left = new TreeNode(3);
    expect(maxDepth(root)).toBe(3);
  });

  test('right-skewed tree', () => {
    const root = new TreeNode(1);
    root.right = new TreeNode(2);
    root.right.right = new TreeNode(3);
    expect(maxDepth(root)).toBe(3);
  });

  test('balanced tree', () => {
    const root = new TreeNode(1);
    root.left = new TreeNode(2);
    root.right = new TreeNode(3);
    root.left.left = new TreeNode(4);
    root.right.right = new TreeNode(5);
    expect(maxDepth(root)).toBe(3);
  });
});