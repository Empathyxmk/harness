import pytest
from unittest import mock

class WebHandler:
    def on_target_not_found(self, context, uri, extras, flags=None):
        uri_str = str(uri)
        if uri_str.startswith("http://") or uri_str.startswith("https://"):
            intent = mock.Mock()
            intent.getStringExtra = mock.Mock(return_value=uri_str)
            intent.getFlags = mock.Mock(return_value=flags if flags is not None else 0)
            context.startActivity(intent)
            return True
        return False

def test_webhandler_on_target_not_found_web_scheme_without_flags_public():
    context = mock.Mock()
    extras = {}
    handler = WebHandler()
    web_uri = "http://public-example.org"
    non_web_uri = "customscheme://baz"
    result = handler.on_target_not_found(context, web_uri, extras)
    assert result is True
    context.startActivity.assert_called_once()

def test_webhandler_on_target_not_found_web_scheme_with_flags_public():
    context = mock.Mock()
    extras = {}
    handler = WebHandler()
    web_uri = "http://public-example.org"
    FLAG_ACTIVITY_REORDER_TO_FRONT = 0x00002000
    result = handler.on_target_not_found(context, web_uri, extras, FLAG_ACTIVITY_REORDER_TO_FRONT)
    assert result is True
    context.startActivity.assert_called_once()
    sent_intent = context.startActivity.call_args[0][0]
    assert sent_intent.getStringExtra("url") == web_uri
    assert sent_intent.getFlags() == FLAG_ACTIVITY_REORDER_TO_FRONT

def test_webhandler_on_target_not_found_non_web_scheme_public():
    context = mock.Mock()
    extras = {}
    handler = WebHandler()
    non_web_uri = "customscheme://baz"
    result = handler.on_target_not_found(context, non_web_uri, extras)
    assert result is False
    context.startActivity.assert_not_called()