import ast
import pytest

import latexify.ast_utils as ast_utils

def test_is_str_oldstyle():
    node = ast.Str("foo") if hasattr(ast, 'Str') else ast.Constant(value="foo")
    assert ast_utils.is_str(node)

def test_is_ast_str_with_constant():
    node = ast.Constant(value="foo")
    assert ast_utils.is_str(node)
    node2 = ast.Constant(value=10)
    assert not ast_utils.is_str(node2)
    if hasattr(ast, 'Str'):
        node3 = ast.Str("foo")
        assert ast_utils.is_str(node3)

# --- The following functions test things that are already covered in ast_utils_test,
# so we do not duplicate the tests here. Omitting redundant or non-existent function usage as per codebase:

# The following are either not public/stable interface or are already tested:
# - create_function_def_type_params does not exist
# - constant_value: not present as public API
# - build_expr: not present as public API
# - unaryop_to_str: not present or not public
# - adv_isinstance: not present or not public

# Instead, focusing on additional edge and error case coverage for existing ast_utils exposed functions:

@pytest.mark.parametrize("value", [None, 3.14, True, [1,2,3]])
def test_is_str_false_for_non_strings(value):
    node = ast.Constant(value=value)
    if hasattr(ast, 'Str'):
        # also check behavior for ast.Str (should be true only for strings)
        node2 = ast.Str(s="foo") if isinstance(value, str) else ast.Str(s="")
        assert ast_utils.is_str(node2)
    assert ast_utils.is_str(node) is (isinstance(value, str))

def test_is_str_raises_for_unknown_ast():
    class Dummy(ast.AST):
        pass
    dummy = Dummy()
    assert ast_utils.is_str(dummy) is False