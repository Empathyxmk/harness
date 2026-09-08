import pytest
from src.path_planning.rrt import RRT

def makeNode(id, x, y, parentID=0):
    n = RRT.rrtNode(id, x, y, parentID)
    return n

def test_default_constructor():
    rrt = RRT()
    tree = rrt.getTree()
    assert len(tree) == 1
    assert tree[0].posX == 0
    assert tree[0].posY == 0

def test_param_constructor():
    rrt = RRT(1.5, 2.2)
    tree = rrt.getTree()
    assert len(tree) == 1
    assert tree[0].posX == 1.5
    assert tree[0].posY == 2.2

def test_add_and_get_node():
    rrt = RRT()
    node = makeNode(1, 2, 3, 0)
    rrt.addNewNode(node)
    assert rrt.getTreeSize() == 2
    n = rrt.getNode(1)
    assert n.posX == 2
    assert n.posY == 3
    assert n.nodeID == 1

def test_remove_node():
    rrt = RRT()
    node = makeNode(1, 3.0, 4.0, 0)
    rrt.addNewNode(node)
    assert rrt.getTreeSize() == 2
    removed = rrt.removeNode(1)
    assert removed.posX == 3.0
    assert rrt.getTreeSize() == 1

def test_set_and_get_pos():
    rrt = RRT()
    rrt.setPosX(0, 5.5)
    rrt.setPosY(0, 6.6)
    assert rrt.getPosX(0) == pytest.approx(5.5)
    assert rrt.getPosY(0) == pytest.approx(6.6)

def test_parent_and_children():
    rrt = RRT()
    node = makeNode(1, 9, 9, 0)
    rrt.addNewNode(node)
    rrt.setParentID(1, 0)
    assert rrt.getNode(1).parentID == 0
    rrt.addChildID(0, 1)
    children = rrt.getChildren(0)
    assert children
    assert children[0] == 1
    assert rrt.getChildrenSize(0) == 1
    parent = rrt.getParent(1)
    assert parent.nodeID == 0

def test_nearest_node_id():
    rrt = RRT()
    rrt.addNewNode(makeNode(1, 10, 10, 0))
    nearest = rrt.getNearestNodeID(9, 9)
    assert nearest == 1
    nearest = rrt.getNearestNodeID(0, 0)
    assert nearest == 0

def test_set_tree():
    rrt = RRT()
    v = [makeNode(5, 11, 22, 0)]
    rrt.setTree(v)
    tree = rrt.getTree()
    assert len(tree) == 1
    assert tree[0].nodeID == 5