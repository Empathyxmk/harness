import pytest
from unittest.mock import Mock

@pytest.fixture
def register_block_type():
    mock_register = Mock()
    mock_create_element = Mock()
    def edit(props):
        value = props['attributes']['content']
        out_props = {
            'tagName': props.get('tagName', 'a'),
            'className': props.get('className', ''),
            'value': value,
            'placeholder': 'Type your tweet...',
            'onFocus': None,
            'onChange': lambda v: props['setAttributes']({'content': v}) if 'setAttributes' in props else None
        }
        mock_create_element('Editable', out_props)
    def save(props):
        className = props.get('className', '')
        value = props['attributes']['content']
        print("Saving tweet block:", value)
        mock_create_element(
            'a',
            {'className': className, 'target': '_blank', 'href': f"https://twitter.com/intent/tweet?text={value}"},
            value
        )
    mock_register('gb/tweet-04', {'title': 'Tweet Block', 'edit': edit, 'save': save})
    return mock_register, mock_create_element

def test_registers_the_block_and_has_expected_settings(register_block_type):
    mock_register, _ = register_block_type
    assert mock_register.call_count == 1
    assert mock_register.call_args[0][0] == 'gb/tweet-04'
    settings = mock_register.call_args[0][1]
    assert isinstance(settings['title'], str)

def test_edit_calls_editable_with_expected_props(register_block_type):
    mock_register, mock_create_element = register_block_type
    settings = mock_register.call_args[0][1]
    set_attributes = Mock()
    props = {
        'className': 'tweet-class',
        'attributes': {'content': 'tweet!'},
        'setAttributes': set_attributes
    }
    mock_create_element.reset_mock()
    settings['edit'](props)
    mock_create_element.assert_called_once()
    _, out_props = mock_create_element.call_args[0][:2]
    assert out_props['className'] == 'tweet-class'
    assert out_props['value'] == 'tweet!'
    assert isinstance(out_props['placeholder'], str)
    assert isinstance(out_props['tagName'], str)

def test_save_encodes_and_renders_a_with_content(register_block_type, capsys):
    mock_register, mock_create_element = register_block_type
    settings = mock_register.call_args[0][1]
    props = {'className': 'hello-tweet', 'attributes': {'content': 'tweet me!'}}
    mock_create_element.reset_mock()
    settings['save'](props)
    out = capsys.readouterr().out
    assert "Saving tweet block:" in out
    mock_create_element.assert_called()
    call_args = mock_create_element.call_args[0]
    assert call_args[0] == 'a'
    args_dict = call_args[1]
    assert args_dict['className'] == 'hello-tweet'
    assert args_dict['target'] == '_blank'
    assert isinstance(args_dict['href'], str)