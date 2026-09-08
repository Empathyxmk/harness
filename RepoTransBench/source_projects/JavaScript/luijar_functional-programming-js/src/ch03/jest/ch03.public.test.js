/**
 * Public test for ch03/model/Node.js, Tree.js - custom data
 */

const { Node } = require('../model/Node');
const { Tree } = require('../model/Tree');

describe('Chapter 3 Node/Tree (public test)', () => {
  test('should create a node with different value', () => {
    const node = new Node(99);
    expect(node.value).toBe(99);
    expect(node.left).toBeNull();
    expect(node.right).toBeNull();
  });

  test('should insert and find different values in a binary tree (public)', () => {
    const tree = new Tree();
    tree.insert(42);
    tree.insert(101);
    expect(tree.contains(42)).toBe(true);
    expect(tree.contains(101)).toBe(true);
    expect(tree.contains(7)).toBe(false);
  });
});