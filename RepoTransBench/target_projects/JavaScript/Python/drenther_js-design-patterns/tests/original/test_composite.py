def import_composite():
    from src.Structural.Composite import Component, Composite, Leaf
    return Component, Composite, Leaf

def test_composite_component_with_no_children():
    Component, Composite, Leaf = import_composite()
    root = Composite('root')
    assert root.__class__.__name__ == 'Composite'
    assert root.get_type() == 'Composite Node'
    assert root.get_node_name() == 'root'
    assert root.no_of_children() == 0

def test_leaf_component():
    Component, Composite, Leaf = import_composite()
    leaf = Leaf('leaf')
    assert leaf.__class__.__name__ == 'Leaf'
    assert leaf.get_type() == 'Leaf Node'
    assert leaf.get_node_name() == 'leaf'
    assert leaf.no_of_children() == 0

def test_should_add_child():
    Component, Composite, Leaf = import_composite()
    node = Composite('node')
    node.add_child(Leaf('left'))
    assert node.no_of_children() == 1
    node.add_child(Leaf('right'))
    assert node.no_of_children() == 2

def test_remove_child_by_name():
    Component, Composite, Leaf = import_composite()
    node = Composite('node')
    node.add_child(Leaf('left'))
    node.add_child(Composite('right'))
    assert node.no_of_children() == 2
    node.remove_child_by_name('right')
    assert node.no_of_children() == 1

def test_remove_child_by_index():
    Component, Composite, Leaf = import_composite()
    node = Composite('node')
    node.add_child(Leaf('left'))
    node.add_child(Composite('middle'))
    node.add_child(Leaf('right'))
    assert node.no_of_children() == 3
    node.remove_child_by_index(1)
    assert node.no_of_children() == 2

def test_log_tree_structure():
    Component, Composite, Leaf = import_composite()
    tree = Composite('root')
    tree.add_child(Leaf('left'))
    right = Composite('right')
    tree.add_child(right)
    right.add_child(Leaf('right-left'))
    right_mid = Composite('right-middle')
    right.add_child(right_mid)
    right.add_child(Leaf('right-right'))
    right_mid.add_child(Leaf('left-end'))
    right_mid.add_child(Leaf('right-end'))
    assert Component.log_tree_structure(tree) == \
        'root\n--left\n--right\n----right-left\n----right-middle\n------left-end\n------right-end\n----right-right\n'