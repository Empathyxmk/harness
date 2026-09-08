import pytest

def test_get_message_public():
    from src.lunar import I18n
    assert I18n.get_message('not_in_table', {"x": 1}) == 'not_in_table'