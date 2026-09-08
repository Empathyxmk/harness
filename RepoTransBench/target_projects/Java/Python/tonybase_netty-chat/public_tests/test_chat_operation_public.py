import pytest
from unittest.mock import Mock

# Minimal stubs for integration with tested logic
class Operation:
    def op(self) -> int:
        pass

class ChatOperation:
    def __init__(self):
        self.applicationContext = None
        self._ops = None

    def operations(self):
        if self._ops is not None:
            return self._ops
        beans = self.applicationContext.getBeansOfType(Operation)
        self._ops = {}
        for bean in beans.values():
            if bean is not None:
                self._ops[bean.op()] = bean
        return self._ops

    def find(self, op):
        ops = self.operations()
        return ops.get(op, None)

@pytest.fixture
def chat_operation_public_setup():
    chat_operation = ChatOperation()
    context = Mock()
    chat_operation.applicationContext = context
    return chat_operation, context

def test_public_operations_empty(chat_operation_public_setup):
    chat_operation, context = chat_operation_public_setup
    context.getBeansOfType.return_value = {'noItem': None}
    ops = chat_operation.operations()
    assert ops is not None
    # Should only add non-null Operation, so map should stay empty or only contain None values
    assert len(ops) == 0 or all(op is None for op in ops.values())

def test_public_operations_with_one_operation_different_op_number(chat_operation_public_setup):
    chat_operation, context = chat_operation_public_setup
    op = Mock(spec=Operation)
    op.op.return_value = 22
    beans = {'otherOp': op}
    context.getBeansOfType.return_value = beans

    ops = chat_operation.operations()
    assert ops is not None
    assert len(ops) == 1
    assert ops[22] is op

def test_public_find(chat_operation_public_setup):
    chat_operation, context = chat_operation_public_setup
    op = Mock(spec=Operation)
    op.op.return_value = 42
    beans = {'deepOp': op}
    context.getBeansOfType.return_value = beans

    chat_operation.operations()
    assert chat_operation.find(42) is op
    assert chat_operation.find(-1) is None