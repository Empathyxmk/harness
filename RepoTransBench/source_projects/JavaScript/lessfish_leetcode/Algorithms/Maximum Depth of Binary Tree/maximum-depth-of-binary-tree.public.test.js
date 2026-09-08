const maxDepth = require('./maximum-depth-of-binary-tree');

function TreeNode(val) {
  this.val = val;
  this.left = this.right = null;
}

describe('maxDepth (public)', () => {
  test('null root returns 0 (again)', () => {
    expect(maxDepth(null)).toBe(0);
  });

  test('single node with a different value', () => {
    const root = new TreeNode(7);
    expect(maxDepth(root)).toBe(1);
  });

  test('tree with three levels, mixed left and right', () => {
    const root = new TreeNode(2);
    root.right = new TreeNode(3);
    root.right.left = new TreeNode(9);
    expect(maxDepth(root)).toBe(3);
  });

  test('more left-skewed tree', () => {
    const root = new TreeNode(5);
    root.left = new TreeNode(6);
    root.left.left = new TreeNode(8);
    root.left.left.left = new TreeNode(10);
    expect(maxDepth(root)).toBe(4);
  });

  test('right-skewed with 4 levels', () => {
    const root = new TreeNode(1);
    root.right = new TreeNode(5);
    root.right.right = new TreeNode(6);
    root.right.right.right = new TreeNode(7);
    expect(maxDepth(root)).toBe(4);
  });

  test('more complex balanced tree', () => {
    const root = new TreeNode(1);
    root.left = new TreeNode(2);
    root.right = new TreeNode(3);
    root.left.right = new TreeNode(4);
    root.right.left = new TreeNode(8);
    root.right.right = new TreeNode(9);
    expect(maxDepth(root)).toBe(3);
  });
});