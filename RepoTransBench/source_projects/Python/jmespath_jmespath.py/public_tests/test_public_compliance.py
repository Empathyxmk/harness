import jmespath


def test_basic_compliance_public():
    data = {"foo": {"bar": 14}}
    result = jmespath.search("foo.bar", data)
    assert result == 14


def test_compliance_index_public():
    data = {"array": [10, 20, 30]}
    assert jmespath.search("array[2]", data) == 30


def test_compliance_current_node_public():
    data = {"a": 1, "b": 2}
    assert jmespath.search("@.b", data) == 2


def test_compliance_multiselect_list_public():
    data = {"a": 9, "b": 7}
    result = jmespath.search("[a, b]", data)
    assert result == [9, 7]