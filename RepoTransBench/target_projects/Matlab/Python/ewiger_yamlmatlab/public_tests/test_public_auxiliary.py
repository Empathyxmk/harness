from yamlmatlab import yaml

def test_vector_matrix_checks():
    r = [9, 8, 7]
    c = [[2], [4], [8]]
    m = [[11, 13], [17, 19]]
    assert yaml.isrowvector(r)
    assert not yaml.isrowvector(c)
    assert yaml.iscolumnvector(c)
    assert not yaml.iscolumnvector(r)
    assert yaml.ismymatrix(m)
    assert not yaml.ismymatrix(c)

def test_issingle_isord():
    import numpy as np
    a = np.float32(5)
    b = 5
    assert yaml.issingle(a)
    assert not yaml.issingle(b)
    assert yaml.isord('banana')
    assert not yaml.isord(['a', 'b'])