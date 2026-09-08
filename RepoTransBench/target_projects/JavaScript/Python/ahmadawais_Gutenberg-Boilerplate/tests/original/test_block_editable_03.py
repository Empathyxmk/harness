import pytest
from unittest.mock import Mock

@pytest.fixture
def register_block_type():
    mock_register = Mock()
    mock_create_element = Mock()
    def edit(props):
        # Emulate Editable block rendering with props
        value = props['attributes']['content']
        out_props = {
            'tagName': 'p',
            'className': props.get('className', ''),
            'value': value,
            'focus': props.get('focus', True),
            'placeholder': props.get('placeholder', None),
            'onFocus': props.get('onFocus', None),
            'onChange': lambda v: props['setAttributes']({'content': v}) if 'setAttributes' in props else None
        }
        mock_create_element('Editable', out_props)
    def save(props):
        className = props.get('className', '')
        value = props['attributes']['content']
        print("Block saving: ", value)
        mock_create_element('p', {'className': className}, value)
    # Register block (emulate JS)
    mock_register('gb/block-editable-03', {'edit': edit, 'save': save})
    return mock_register, mock_create_element

def test_registers_block_and_has_expected_structure(register_block_type):
    mock_register, _ = register_block_type
    assert mock_register.call_count == 1
    args = mock_register.call_args[0]
    assert args[0] == 'gb/block-editable-03'
    settings = args[1]
    assert callable(settings['edit'])
    assert callable(settings['save'])

def test_edit_renders_editable_element_with_expected_props_and_onchange(register_block_type):
    mock_register, mock_create_element = register_block_type
    settings = mock_register.call_args[0][1]
    set_attributes = Mock()
    props = {
        'className': 'ed-class',
        'focus': True,
        'attributes': {'content': 'hello'},
        'setAttributes': set_attributes
    }
    mock_create_element.reset_mock()
    settings['edit'](props)
    mock_create_element.assert_called_once()
    _, out_props = mock_create_element.call_args[0][:2]
    assert out_props['tagName'] == 'p'
    assert out_props['className'] == 'ed-class'
    assert out_props['value'] == 'hello'
    assert out_props['focus'] is True
    _ = out_props.get('placeholder', None)  # just access, should not raise
    # Accept onFocus: function or None
    assert callable(out_props.get('onFocus')) or out_props.get('onFocus') is None
    # onChange triggers setAttributes
    if 'onChange' in out_props and out_props['onChange']:
        out_props['onChange']('zzz')
        set_attributes.assert_called_with({'content': 'zzz'})

def test_save_logs_and_renders_p_element_with_content(register_block_type, capsys):
    mock_register, mock_create_element = register_block_type
    settings = mock_register.call_args[0][1]
    props = {'className': 'from-save', 'attributes': {'content': 'Save test'}}
    mock_create_element.reset_mock()
    settings['save'](props)
    out = capsys.readouterr().out
    assert "Block saving:" in out
    mock_create_element.assert_called_with('p', {'className': 'from-save'}, 'Save test')