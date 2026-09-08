import io
import json
import pytest

from jsoncsv import jsontool

def test_gen_leaf_simple_dict():
    root = {'a': 1, 'b': {'c': 2}}
    leaves = list(jsontool.gen_leaf(root))
    # leaves contain 2 tuples: (['a'],1), (['b','c'],2)
    assert any(p == ['a'] and v == 1 for p,v in leaves)
    assert any(p == ['b','c'] and v == 2 for p,v in leaves)

def test_is_array_index_true_and_false():
    keys = [0,1,2]
    assert jsontool.is_array_index(keys)
    keys2 = [1,0]
    assert jsontool.is_array_index(keys2)
    keys3 = ['0','1']
    assert jsontool.is_array_index(keys3)
    keys4 = ['a','b']
    assert not jsontool.is_array_index(keys4)

def test_from_leaf_dict_and_list():
    # dict case
    leafs = [ (['a'], 1), (['b'], 2)]
    val = jsontool.from_leaf([ [k[:], v] for k,v in leafs ])
    assert isinstance(val, dict)
    # list case
    leafs = [ ([0], "a"), ([1], "b") ]
    val2 = jsontool.from_leaf([ [k[:], v] for k,v in leafs ])
    assert isinstance(val2, list)

def test_expand_and_restore_roundtrip():
    d = {"a": 1, "b": {"c": 2}}
    exp = jsontool.expand(d)
    rest = jsontool.restore(exp)
    assert rest == d

def test_expand_safe_and_restore_safe():
    d = {"x.y": {"z": 1}}
    exp = jsontool.expand(d, safe=True)
    rest = jsontool.restore(exp, safe=True)
    assert rest == d

def test_convert_json_expand_and_restore(tmp_path):
    # Use file objects to test writing
    fdin = tmp_path / "in.json"
    fdout = tmp_path / "out.json"
    # write two lines
    fdin.write_text('{"x":1}\n{"y":2}\n')
    with fdin.open("r", encoding="utf-8") as fin, fdout.open("w", encoding="utf-8") as fout:
        jsontool.convert_json(fin, fout, jsontool.expand)
    # now restore
    with fdout.open("r", encoding="utf-8") as fin, (tmp_path / "restore.json").open("w", encoding="utf-8") as fout:
        jsontool.convert_json(fin, fout, jsontool.restore)
    # final file should be jsons
    lines = (tmp_path / "restore.json").read_text().splitlines()
    for line in lines:
        obj = json.loads(line)
        assert isinstance(obj, dict)

def test_convert_json_invalid_func():
    fin = io.StringIO('{"x":1}\n')
    fout = io.StringIO()
    with pytest.raises(ValueError):
        jsontool.convert_json(fin, fout, None)

def test_convert_json_json_array(tmp_path):
    arr = [ {"foo":1}, {"bar":2} ]
    fnin = tmp_path / "arr.json"
    fnin.write_text(json.dumps(arr))
    fnout = tmp_path / "outarr.json"
    with fnin.open("r", encoding="utf-8") as fin, fnout.open("w", encoding="utf-8") as fout:
        jsontool.convert_json(fin, fout, jsontool.expand, json_array=True)
    # Should correctly output both objects
    lines = fnout.read_text().splitlines()
    assert len(lines) == 2
    for l in lines:
        assert "foo" in l or "bar" in l