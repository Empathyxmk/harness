import jmespath

def test_compliance_branch_array_public():
    data = {"x": [3, 4, 5]}
    result = jmespath.search("x[1]", data)
    assert result == 4

def test_compliance_branch_multiselect_object_public():
    data = {"foo": 22, "bar": 33}
    res = jmespath.search("{q: foo, r: bar}", data)
    assert res == {"q": 22, "r": 33}