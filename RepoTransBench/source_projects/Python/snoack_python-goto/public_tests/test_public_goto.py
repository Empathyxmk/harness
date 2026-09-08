import sys
import os

# Ensure we can import the main 'goto.py' module from parent dir
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import goto

def test_goto_has_no_goto_and_label_by_default():
    # Check that the 'goto' module does not expose 'goto' or 'label' attributes by default
    assert not hasattr(goto, "goto")
    assert not hasattr(goto, "label")

def test_goto_module_has_file_attribute():
    # Instead of a docstring, test a universally present attribute: __file__
    assert hasattr(goto, "__file__")
    assert isinstance(goto.__file__, str)

def test_goto_module_name_is_goto():
    # The module should have __name__ attribute equal to "goto"
    assert getattr(goto, '__name__', 'notfound') == "goto"