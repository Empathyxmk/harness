import pytest

from forms_builder.forms import fields
from forms_builder.forms import utils
from forms_builder.forms.settings import USE_SITES, USE_THREADED_EMAILS, EXTRA_FIELD_TYPES

def test_field_choices_dict():
    choices = "Red\nGreen\nBlue"
    expected = [("Red", "Red"), ("Green", "Green"), ("Blue", "Blue")]
    assert fields.choices_from_lines(choices) == expected

def test_field_choices_dict_empty():
    assert fields.choices_from_lines("") == []

def test_is_file():
    assert utils.is_file("photo.PNG")
    assert utils.is_file("document.PDF")
    assert not utils.is_file("example.txt")
    assert not utils.is_file("no_dot")

def test_slugify_strip_and_lower():
    s = " Hello__World__ "
    sl = utils.slugify(s)
    assert sl == "hello-world"

def test_setting_imports():
    assert isinstance(USE_SITES, bool)
    assert isinstance(USE_THREADED_EMAILS, bool)
    assert isinstance(EXTRA_FIELD_TYPES, list)