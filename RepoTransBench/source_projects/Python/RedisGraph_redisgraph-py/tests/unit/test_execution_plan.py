import pytest
from redisgraph.execution_plan import ProfileStats, Operation, ExecutionPlan

def test_profile_stats_fields():
    ps = ProfileStats(10, 1.23)
    assert ps.records_produced == 10
    assert ps.execution_time == 1.23

def test_operation_eq_and_str():
    op1 = Operation("Filter")
    op2 = Operation("Filter")
    op3 = Operation("Scan")
    op4 = Operation("Filter", args="x > 1")
    assert op1 == op2
    assert not (op1 == op3)
    assert not (op1 == op4)
    assert str(op1) == "Filter"
    assert str(op4) == "Filter | x > 1"

def test_operation_append_and_child_count():
    op = Operation("Root")
    child = Operation("Child")
    op.append_child(child)
    assert op.child_count() == 1
    assert op.children[0] is child

    with pytest.raises(Exception):
        op.append_child(op)
    with pytest.raises(Exception):
        op.append_child("not_op")

def test_execution_plan_eq_and_str_patch_tree():
    # Patch to avoid real parsing (which expects a RedisGraph plan format)
    class DummyEP(ExecutionPlan):
        def _operation_tree(self):
            op1 = Operation("Root")
            op2 = Operation("Child")
            op1.append_child(op2)
            return op1
    ep1 = DummyEP([])
    ep2 = DummyEP([])
    assert ep1 == ep2
    assert isinstance(str(ep1), str)

    class OtherEP(ExecutionPlan):
        def _operation_tree(self):
            return Operation("DifferentRoot")
    ep3 = OtherEP([])
    assert not (ep1 == ep3)

def test_execution_plan_invalid_init():
    with pytest.raises(Exception):
        ExecutionPlan("notalist")

def test_operation_traverse_manual_tree():
    # Test operation traverse using a manual tree, patching structured_plan
    class DummyEP(ExecutionPlan):
        def _operation_tree(self):
            op = Operation("A")
            opB = Operation("B")
            opC = Operation("C")
            op.append_child(opB)
            op.append_child(opC)
            return op
    ep = DummyEP([])
    result = ep._operation_traverse(
        ep.structured_plan, lambda x: x.name, lambda c: ','.join(c), lambda x, y: f"{x}>{y}"
    )
    assert result == "A>B,C"

@pytest.mark.parametrize("plan,expected_name", [
    (
        [
            "Project",
            "    Filter  (predicate: (n.v > 1))",
            "        NodeByLabelScan | (n:V)"
        ],
        "Project"
    ),
    (
        [
            "Filter",
            "    NodeByLabelScan | (n:V)"
        ],
        "Filter"
    )
])
def test_operation_tree_simple(monkeypatch, plan, expected_name):
    # Monkeypatch ProfileStats to None to skip "Records produced" parsing
    ep = ExecutionPlan(plan)
    assert isinstance(ep.structured_plan, Operation)
    assert ep.structured_plan.name == expected_name