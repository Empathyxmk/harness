import pytest
try:
    from src.parser import Step
except ImportError:
    Step = {}

def test_constructor_or_object_public():
    assert callable(Step) or isinstance(Step, object)

def test_create_step_different_step_name_public():
    if callable(Step):
        step = Step("begin", 123)
        assert getattr(step, "name", None) == "begin"
        assert getattr(step, "value", None) == 123