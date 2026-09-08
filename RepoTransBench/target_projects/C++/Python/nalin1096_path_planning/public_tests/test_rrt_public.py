import pytest
from src.path_planning.rrt import RRT

def makeNodePublic(id, x, y, parentID=0):
    return RRT.rrtNode(id, x, y, parentID)

def test_default_constructor_public():
    rrt = RRT()
    tree = rrt.getTree()
    assert len(tree) == 1
    assert tree[0].posX == 0
    assert tree[0].posY == 0

def test_param_constructor_different():
    rrt = RRT(-3.7, 4.3)
    tree = rrt.getTree()
    assert len(tree) == 1
    assert tree[0].posX == -3.7
    assert tree[0].posY == 4.3

def test_add_and_get_node_different():
    rrt = RRT()
    node = makeNodePublic(1, -4, -9, 0)
    rrt.addNewNode(node)
    assert rrt.getTreeSize() == 2
    n = rrt.getNode(1)
    assert n.posX == -4
    assert n.posY == -9
    assert n.nodeID == 1

def test_remove_node_different():
    rrt = RRT()
    node = makeNodePublic(2, 7.5, 8.5, 0)
    rrt.addNewNode(node)
    assert rrt.getTreeSize() == 2
    removed = rrt.removeNode(2)
    assert removed.posX == 7.5
    assert rrt.getTreeSize() == 1

def test_set_and_get_pos_different():
    rrt = RRT()
    rrt.setPosX(0, -2.2)
    rrt.setPosY(0, -6.1)
    assert rrt.getPosX(0) == pytest.approx(-2.2)
    assert rrt.getPosY(0) == pytest.approx(-6.1)

def test_parent_and_children_different():
    rrt = RRT()
    node = makeNodePublic(3, -9, 12, 0)
    rrt.addNewNode(node)
    rrt.setParentID(3, 0)
    assert rrt.getNode(3).parentID == 0
    rrt.addChildID(0, 3)
    children = rrt.getChildren(0)
    assert children
    assert children[0] == 3
    assert rrt.getChildrenSize(0) == 1
    parent = rrt.getParent(3)
    assert parent.nodeID == 0

def test_nearest_node_id_different():
    rrt = RRT()
    rrt.addNewNode(makeNodePublic(8, -20, 21, 0))
    nearest = rrt.getNearestNodeID(-19, 23)
    assert nearest == 8
    nearest = rrt.getNearestNodeID(0, 0)
    assert nearest == 0

def test_set_tree_different():
    rrt = RRT()
    v = [makeNodePublic(25, 33, 77, 0)]
    rrt.setTree(v)
    tree = rrt.getTree()
    assert len(tree) == 1
    assert tree[0].nodeID == 25