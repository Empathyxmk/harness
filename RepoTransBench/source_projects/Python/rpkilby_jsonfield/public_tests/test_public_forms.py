import pytest
from src.jsonfield.forms import JSONFormField
from django import forms

class DummyForm(forms.Form):
    payload = JSONFormField(required=False)

def test_blank_form():
    # Different from original: test with required=False & blank POST
    form = DummyForm({})
    assert form.is_valid()
    assert form.cleaned_data['payload'] is None

def test_valid_json_form_value():
    # Use a different valid value
    form = DummyForm({'payload': '{"species": "cat", "legs": 4}'})
    assert form.is_valid()
    cd = form.cleaned_data['payload']
    assert cd == {'species': "cat", 'legs': 4}

def test_invalid_json_form_value():
    form = DummyForm({'payload': '{"species": unquoted}'})
    assert not form.is_valid()
    assert 'payload' in form.errors

def test_python_obj_input():
    # Pass a dict directly
    form = DummyForm({'payload': {'key': [1, 2]}})
    assert form.is_valid()
    assert form.cleaned_data['payload'] == {'key': [1, 2]}