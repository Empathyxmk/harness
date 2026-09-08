import sys
import os
import pytest

# Ensure redisgraph module is found when running from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redisgraph.execution_plan import ProfileStats, Operation, ExecutionPlan

def test_public_profilestats_repr_and_equality():
    # Use different numeric values than in existing tests
    stats1 = ProfileStats(records=23, execution_time=11.7, child_stats=None)
    stats2 = ProfileStats(records=23, execution_time=11.7, child_stats=None)
    stats3 = ProfileStats(records=29, execution_time=13.2, child_stats=None)
    assert repr(stats1) == repr(stats2)
    assert stats1 == stats2
    assert stats1 != stats3

def test_public_operation_hierarchy():
    op = Operation(name='OpA', args={'cost': 2}, children=[])
    op_child = Operation(name='OpB', args={'cost': 3}, children=[])
    op.add_child(op_child)
    assert op.children[0] == op_child
    assert op.to_dict()['name'] == 'OpA'

def test_public_executionplan_repr():
    stats = ProfileStats(records=7, execution_time=1.9, child_stats=None)
    op = Operation(name='Scan', args={}, children=[])
    ep = ExecutionPlan(root_operation=op, profile_stats=stats)
    assert 'Scan' in repr(ep)
    assert 'records=7' in repr(ep)