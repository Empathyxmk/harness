def public_is_var_function(node):
    if not node:
        return False
    if node.get('type') != 'function':
        return False
    if node.get('value') != 'var':
        return False
    if not isinstance(node.get('nodes'), list):
        return False
    if len(node['nodes']) == 0:
        return False
    return True

def test_is_var_function_returns_false_for_non_var_or_improperly_structured_nodes_public():
    # value is not 'var'
    assert public_is_var_function({'type': 'function', 'value': 'random', 'nodes': [{'type':'word','value':'x'}]}) is False
    # type not 'function'
    assert public_is_var_function({'type': 'word', 'value': 'var', 'nodes': [{'type': 'function'}]}) is False
    # nodes is undefined
    assert public_is_var_function({'type': 'function', 'value': 'var', 'nodes': None}) is False
    # undefined argument
    assert public_is_var_function(None) is False
    # empty nodes array
    assert public_is_var_function({'type': 'function', 'value': 'var', 'nodes': []}) is False

def test_is_var_function_returns_true_for_valid_var_public():
    assert public_is_var_function({'type': 'function', 'value': 'var', 'nodes': [{'type': 'word', 'value': 'yet-different'}]})