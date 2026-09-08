import pytest
from src.como_lang.mocks import COMO_OPCODE_MAX, como_opcode_handler_table, mock_opcode_handler, Object

def test_opcode_handlers_table():
    for i in range(COMO_OPCODE_MAX):
        handler = como_opcode_handler_table[i]
        # In Python, we just check if it's callable and if calling it doesn't break
        assert callable(handler)
        handler(Object(), Object(), Object()) # Call with dummy objects, as in C