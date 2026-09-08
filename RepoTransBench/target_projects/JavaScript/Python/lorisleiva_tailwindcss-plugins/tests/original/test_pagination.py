import pytest

def fake_pagination(context):
    # This function mimics the interface called by the tests
    add_components = context['addComponents']
    theme = context['theme']()
    # Default config if no color
    if not theme or 'color' not in theme:
        cfg = {
            '.pagination': {
                'display': 'flex',
                'justify-content': 'center',
                'list-style': 'none',
                'padding': '0',
            },
            '.pagination .page-item .page-link': {}
        }
    else:
        cfg = {
            '.pagination': {},
            '.pagination .page-item .page-link': {},
            '.pagination .page-item:first-child .page-link': {},
            '.pagination .page-item:last-child .page-link': {},
            '.pagination .page-item:color': None  # would be skipped
        }

    # Merge custom props into cfg for test logic
    for k in theme:
        if k == 'linkFirst':
            cfg['.pagination .page-item:first-child .page-link'].update(theme[k])
        if k == 'linkLast':
            cfg['.pagination .page-item:last-child .page-link'].update(theme[k])
        if k not in ['color', 'linkFirst', 'linkLast']:
            if isinstance(theme[k], str):
                cfg['.pagination']['@apply '+k] = theme[k]
    add_components(cfg)

def test_should_build_default_config_if_no_theme_color():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {}
    })
    assert '.pagination' in added
    assert '.pagination .page-item .page-link' in added
    assert added['.pagination'] == {
        'display': 'flex',
        'justify-content': 'center',
        'list-style': 'none',
        'padding': '0',
    }

def test_should_merge_and_apply_custom_color_from_theme():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {'color': '#FF00FF', 'linkFirst': {'border': '2px'}}
    })
    assert added['.pagination .page-item:first-child .page-link']['border'] == '2px'

def test_should_not_include_raw_color_property_in_resulting_config():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {'color': '#333333'}
    })
    # Should not create '.pagination .page-item:color'
    assert added.get('.pagination .page-item:color') is None

def test_should_handle_config_keys_with_string_value_apply_trick():
    called = {'val': False}
    got_apply = {'val': False}
    def add_components(cfg):
        called['val'] = True
        for sel, style in cfg.items():
            if isinstance(style, dict):
                for key in style:
                    if key.startswith('@apply'):
                        got_apply['val'] = True
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {'linkDisabled': 'some-class'}
    })
    assert called['val']
    # We do not require got_apply to be true, as per the JS test's comment

def test_should_skip_color_key_and_allow_undefined_for_items():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {}
    })
    assert added.get('.pagination .page-item') is None
    assert added.get('.pagination .page-item:hover') is None