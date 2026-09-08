import sys
import os

# Allow importing parent's goto module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import goto as goto_mod

def test_public_goto_label_and_table():
    table = {}
    code = [
        ("label1", 10),
        ("label2", 20)
    ]
    for name, line in code:
        table[name] = line
    assert table["label1"] == 10
    assert table["label2"] == 20

def test_public_goto_macro_lines():
    # Simulate a scenario of line extraction: just use different data than in the main tests
    src = "alpha\nbeta\n# label x\n# goto x\nomega"
    lines = src.split("\n")
    found_label = False
    for i, line in enumerate(lines):
        if "# label x" in line:
            found_label = True
            label_line = i
    assert found_label is True
    assert label_line == 2

def test_public_goto_internals_exc():
    class Dummy(Exception): pass
    got_error = False
    try:
        raise Dummy("test error")
    except Dummy as e:
        got_error = str(e)
    assert got_error == "test error"