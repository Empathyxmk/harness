import io
import json
import pytest

from jsoncsv import jsontool

def test_gen_leaf_simple_dict():
    root = {'x': 100, 'y': {'z': 200}}
    leaves = list(jsontool.gen_leaf(root))
    # leaves contain 2 tuples: (['x'],100), (['y','z'],200)
    assert any(p == ['x'] and v == 100 for p,v in leaves)
    assert any(p == ['y','z'] and v == 200 for p,v in leaves)

def test_is_array_index_true_and_false():
    keys = [9,8,7]
    assert jsontool.is_array_index(keys)
    keys2 = [0,2]
    assert jsontool.is_array_index(keys2)
    keys3 = ['2','3']
    assert jsontool.is_array_index(keys3)
    keys4 = ['q','r']
    assert not jsontool.is_array_index(keys4)

def test_from_leaf_dict_and_list():
    # dict case
    leafs = [ (['x'], 100), (['y'], 200)]
    val = jsontool.from_leaf([ [k[:], v] for k,v in leafs ])
    assert isinstance(val, dict)
    # list case
    leafs = [ ([2], "foo"), ([0], "bar") ]
    val2 = jsontool.from_leaf([ [k[:], v] for k,v in leafs ])
    assert isinstance(val2, list)

def test_expand_and_restore_roundtrip():
    d = {"foo": 99, "bar": {"baz": 88}}
    exp = jsontool.expand(d)
    rest = jsontool.restore(exp)
    assert rest == d

def test_expand_safe_and_restore_safe():
    d = {"site.key": {"deep": 1024}}
    exp = jsontool.expand(d, safe=True)
    rest = jsontool.restore(exp, safe=True)
    assert rest == d

def test_convert_json_expand_and_restore(tmp_path):
    # Use file objects to test writing
    fdin = tmp_path / "in2.json"
    fdout = tmp_path / "out2.json"
    # write two lines
    fdin.write_text('{"foo":5}\n{"bar":7}\n')
    with fdin.open("r", encoding="utf-8") as fin, fdout.open("w", encoding="utf-8") as fout:
        jsontool.convert_json(fin, fout, jsontool.expand)
    # now restore
    with fdout.open("r", encoding="utf-8") as fin, (tmp_path / "restore2.json").open("w", encoding="utf-8") as fout:
        jsontool.convert_json(fin, fout, jsontool.restore)
    # final file should be jsons
    lines = (tmp_path / "restore2.json").read_text().splitlines()
    for line in lines:
        obj = json.loads(line)
        assert isinstance(obj, dict)

def test_convert_json_invalid_func():
    fin = io.StringIO('{"z":900}\n')
    fout = io.StringIO()
    import pytest
    with pytest.raises(ValueError):
        jsontool.convert_json(fin, fout, None)

def test_convert_json_json_array(tmp_path):
    arr = [ {"baz":35}, {"qux":53} ]
    fnin = tmp_path / "arr2.json"
    fnin.write_text(json.dumps(arr))
    fnout = tmp_path / "outarr2.json"
    with fnin.open("r", encoding="utf-8") as fin, fnout.open("w", encoding="utf-8") as fout:
        jsontool.convert_json(fin, fout, jsontool.expand, json_array=True)
    # Should correctly output both objects
    lines = fnout.read_text().splitlines()
    assert len(lines) == 2
    for l in lines:
        assert "baz" in l or "qux" in l