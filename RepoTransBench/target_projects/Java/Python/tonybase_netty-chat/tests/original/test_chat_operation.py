import pytest
from unittest.mock import Mock, patch
import types

# Assume the minimal stubs for classes under test
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
def chat_operation_test_setup():
    chat_operation = ChatOperation()
    context = Mock()
    # Set via attribute directly (Python, no need for reflection)
    chat_operation.applicationContext = context
    return chat_operation, context

def test_operations_empty(chat_operation_test_setup):
    chat_operation, context = chat_operation_test_setup
    context.getBeansOfType.return_value = {}
    ops = chat_operation.operations()
    assert ops is not None
    assert len(ops) == 0

def test_operations_with_one_operation(chat_operation_test_setup):
    chat_operation, context = chat_operation_test_setup
    op = Mock(spec=Operation)
    op.op.return_value = 1
    beans = {'myOp': op}
    context.getBeansOfType.return_value = beans

    ops = chat_operation.operations()
    assert ops is not None
    assert len(ops) == 1
    assert ops[1] is op

def test_find(chat_operation_test_setup):
    chat_operation, context = chat_operation_test_setup
    op = Mock(spec=Operation)
    op.op.return_value = 5
    beans = {'myOp': op}
    context.getBeansOfType.return_value = beans

    chat_operation.operations()
    assert chat_operation.find(5) is op
    assert chat_operation.find(99) is None