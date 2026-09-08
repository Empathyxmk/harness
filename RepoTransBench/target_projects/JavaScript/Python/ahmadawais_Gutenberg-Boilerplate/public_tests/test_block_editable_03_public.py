import pytest
from unittest.mock import Mock

@pytest.fixture
def register_block_type():
    mock_register = Mock()
    mock_create_element = Mock()
    def edit(_self, props):
        value = props['attributes']['content']
        out_props = {
            'tagName': 'p',
            'className': props.get('className', ''),
            'value': value,
        }
        mock_create_element('Editable', out_props)
    mock_register('gb/block-editable-03', {'edit': edit, 'save': lambda props: None})
    block_args = mock_register.call_args[0][1]
    return mock_create_element, block_args["edit"]

def test_edit_renders_editable_with_default_props_and_onchange(register_block_type):
    mock_create_element, editFn = register_block_type
    mock_create_element.reset_mock()
    editFn(None, {
        "className": "custom-public-class",
        "setAttributes": lambda *a, **k: None,
        "attributes": {
            "content": "test-value",
        },
        "setFocus": lambda *a, **k: None,
        "isSelected": True,
        "onChange": lambda *a, **k: None,
        "editableRef": {"current": None}
    })
    mock_create_element.assert_called_once()
    _, out_props = mock_create_element.call_args[0][:2]
    assert out_props["tagName"] == "p"
    assert out_props["className"] == "custom-public-class"
    assert out_props["value"] == "test-value"

def test_edit_renders_editable_with_alternate_props_and_onchange(register_block_type):
    mock_create_element, editFn = register_block_type
    mock_create_element.reset_mock()
    editFn(None, {
        "className": "alt-ed-public",
        "setAttributes": lambda *a, **k: None,
        "attributes": {
            "content": "gutenberg",
        },
        "setFocus": lambda *a, **k: None,
        "isSelected": False,
        "onChange": lambda *a, **k: None,
        "editableRef": {"current": None}
    })
    mock_create_element.assert_called_once()
    _, out_props = mock_create_element.call_args[0][:2]
    assert out_props["tagName"] == "p"
    assert out_props["className"] == "alt-ed-public"
    assert out_props["value"] == "gutenberg"