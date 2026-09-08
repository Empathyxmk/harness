const assert = require('chai').assert;
const TreeModel = require('../index');

describe('TreeModel branch and error PUBLIC coverage', function () {
  it('should instantiate TreeModel with a different config object', function () {
    var tree = new TreeModel({ childrenPropertyName: 'minions' });
    assert.instanceOf(tree, TreeModel);
  });

  it('should parse node with another custom children property', function () {
    var tree = new TreeModel({ childrenPropertyName: 'descendants' });
    var root = tree.parse({ descendants: [{ name: 'foo' }, { name: 'bar' }] });
    assert.equal(root.children.length, 2);
  });

  it('should throw error if parsing various non-object models', function () {
    var tree = new TreeModel();
    assert.throws(() => tree.parse(true), /object/i);
    assert.throws(() => tree.parse(Symbol()), /object/i);
    assert.throws(() => tree.parse([]), /object/i);
    assert.throws(() => tree.parse(function () {}), /object/i);
  });

  it('should return undefined if no child at index for getChildAt (with more children)', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 10}, {id: 20}] });
    assert.isUndefined(root.children[2]);
  });

  it('should check isRoot and hasChildren for different structures', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 101}, {id: 202}] });
    var child = root.children[1];
    assert.isTrue(root.isRoot());
    assert.isTrue(root.hasChildren());
    assert.isFalse(child.isRoot());
    assert.isFalse(child.hasChildren());
  });

  it('should remove a child and update parent/children with multiple children', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 100}, {id: 200}] });
    var child = root.children[1];
    child.drop();
    assert.equal(root.children.length, 1);
    assert.isUndefined(child.parent);
  });

  it('should not remove when calling drop on a fake unattached child', function () {
    var tree = new TreeModel();
    var root = tree.parse({ children: [{id: 5}] });
    var fake = new TreeModel().parse({id: 77});
    assert.doesNotThrow(() => fake.drop());
    assert.equal(root.children.length, 1);
  });

  it('should correctly traverse forEach with other values', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 90, children: [{id: 91}, {id: 92}]});
    let visited = [];
    root.walk(function(node) {
      visited.push(node.model.id);
      return true;
    }, {strategy: 'breadthFirst'});
    assert.sameMembers(visited, [90,91,92]);
  });

  it('should break early forEach if callback returns false on another node', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 50, children: [{id: 51}, {id: 52}]});
    let visited = [];
    root.walk(function(node) {
      visited.push(node.model.id);
      if (node.model.id === 52) return false;
      return true;
    }, {strategy: 'breadthFirst'});
    assert.include(visited, 52);
  });

  it('should filter descendants correctly with different predicate', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 70, children: [{id: 71}, {id: 72}, {id: 68}]});
    var matches = root.all(function (node) { return node.model.id < 72; });
    assert.sameDeepMembers(matches.map(n=>n.model.id), [70,71,68]);
  });

  it('should add a child with addChild and check toString', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 111});
    var child = tree.parse({id: 222});
    root.addChild(child);
    assert.equal(root.children[0].model.id, 222);
    assert.isString(root.toString());
  });

  it('should add a child at different index', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 8, children: [{id: 19}]});
    var child = tree.parse({id: 11});
    root.addChildAtIndex(child, 1);
    assert.equal(root.children[1].model.id, 11);
  });

  it('should handle getIndex with not found child for a different id', function () {
    var tree = new TreeModel();
    var root = tree.parse({id: 44, children: [{id: 99}]});
    var child = tree.parse({id: 77});
    assert.strictEqual(child.getIndex(), 0); // root node index is always 0
    assert.strictEqual(root.children.map(c => c.model.id).indexOf(child.model.id), -1);
  });
});