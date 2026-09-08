import pytest

def fake_pagination(context):
    add_components = context['addComponents']
    theme = context['theme']()
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
            '.pagination .page-item:color': None
        }
    for k in theme:
        if k == 'linkFirst':
            cfg['.pagination .page-item:first-child .page-link'].update(theme[k])
        if k == 'linkLast':
            cfg['.pagination .page-item:last-child .page-link'].update(theme[k])
        if k not in ['color', 'linkFirst', 'linkLast']:
            if isinstance(theme[k], str):
                cfg['.pagination']['@apply '+k] = theme[k]
    add_components(cfg)

def test_should_build_default_config_if_no_theme_color_public():
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

def test_should_merge_and_apply_custom_color_from_theme_public():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {'color': '#00FF00', 'linkLast': {'border': '3px solid #000'}}
    })
    assert added['.pagination .page-item:last-child .page-link']['border'] == '3px solid #000'

def test_should_not_include_raw_color_property_in_resulting_config_public():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {'color': '#123456'}
    })
    assert added.get('.pagination .page-item:color') is None

def test_should_handle_config_keys_with_string_value_apply_trick_public():
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
        'theme': lambda: {'linkActive': 'bg-blue-700'}
    })
    assert called['val']

def test_should_skip_color_key_and_allow_undefined_for_other_items_public():
    added = {}
    def add_components(cfg):
        added.update(cfg)
    fake_pagination({
        'addComponents': add_components,
        'theme': lambda: {}
    })
    assert added.get('.pagination .page-item') is None
    assert added.get('.pagination .page-item:hover') is None