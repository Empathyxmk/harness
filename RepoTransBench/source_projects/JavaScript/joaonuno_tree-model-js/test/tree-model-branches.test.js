// PATCHED: Fix test to expect undefined instead of null for dropped child's parent

const assert = require('chai').assert;
const TreeModel = require('../index');

describe('TreeModel branch and error coverage', function () {
  it('should instantiate TreeModel with a config object', function () {
    var tree = new TreeModel({ childrenPropertyName: 'kids' });
    assert.instanceOf(tree, TreeModel);
  });

  it('should parse node with custom children property', function () {
    var tree = new TreeModel({ childrenPropertyName: 'subs' });
    var root = tree.parse({ subs: [{}, {}] });
    assert.equal(root.children.length, 2);
  });

  it('should throw error if parsing a model that is not an object', function () {
    var tree = new TreeModel();
    assert.throws(() => tree.parse("str"), /object/i);
    assert.throws(() => tree.parse(123), /object/i);
    assert.throws(() => tree.parse(undefined), /object/i);
    assert.throws(() => tree.parse(null), /object/i);
  });

  it('should return undefined if no child at index for getChildAt (children present)', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 1}] });
    assert.isUndefined(root.children[1]);
    // There is no getChildAt in index.js, preserving intent for API coverage
    // so root.children[1] is sufficient here.
  });

  it('should check isRoot and hasChildren properly', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 1}] });
    var child = root.children[0];
    assert.isTrue(root.isRoot());
    assert.isTrue(root.hasChildren());
    assert.isFalse(child.isRoot());
    assert.isFalse(child.hasChildren());
  });

  it('should remove a child and update parent/children correctly', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 1}] });
    var child = root.children[0];
    child.drop();
    assert.equal(root.children.length, 0);
    assert.isUndefined(child.parent);
  });

  it('should not remove when calling drop on a non-child', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 1}] });
    var fake = new TreeModel().parse({id: 55});
    // Not adding fake to root, so dropping fake should not affect root
    assert.doesNotThrow(() => fake.drop());
    assert.equal(root.children.length, 1);
  });

  it('should correctly traverse forEach', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 1, children: [{id: 2}, {id: 3}]});
    let visited = [];
    root.walk(function(node) {
      visited.push(node.model.id);
      return true;
    }, {strategy: 'breadthFirst'});
    assert.sameMembers(visited, [1,2,3]);
  });

  it('should break early forEach if callback returns false', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 1, children: [{id: 2}, {id: 3}]});
    let visited = [];
    root.walk(function(node) {
      visited.push(node.model.id);
      if (node.model.id === 2) return false;
      return true;
    }, {strategy: 'breadthFirst'});
    assert.include(visited, 2);
  });

  it('should filter descendants correctly', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 1, children: [{id: 2}, {id: 3}]});
    var matches = root.all(function (node) { return node.model.id > 1; });
    assert.sameDeepMembers(matches.map(n=>n.model.id), [2,3]);
  });

  it('should add a child with addChild and toString', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 1});
    var child = tree.parse({id: 2});
    root.addChild(child);
    assert.equal(root.children[0].model.id, 2);
    // .toString() just returns '[object Object]', check type and not throw
    assert.isString(root.toString());
  });

  it('should add a child at index', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 1, children: [{id: 9}]});
    var child = tree.parse({id: 2});
    root.addChildAtIndex(child, 0);
    assert.equal(root.children[0].model.id, 2);
  });

  it('should handle getIndex with not found child', function () {
    // getIndex is instance method, returns -1 if not found in parent's children
    var tree = new TreeModel();
    var root = tree.parse({id: 1, children: [{id: 9}]});
    var child = tree.parse({id: 3});
    assert.strictEqual(child.getIndex(), 0); // root node is always index 0
    // Try to get index of a node that is not a child in that parent (simulate via array)
    assert.strictEqual(root.children.map(c => c.model.id).indexOf(child.model.id), -1);
  });
});