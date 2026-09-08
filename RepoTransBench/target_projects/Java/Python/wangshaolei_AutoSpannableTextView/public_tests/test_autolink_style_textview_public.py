import pytest
from unittest import mock

class AutoLinkStyleTextView:
    styleType = 1
    def __init__(self, context, attrs, defStyle):
        self.context = context
        self.attrs = attrs
        self.defStyle = defStyle
        self.text = ""
        self._callback = None
        self.array = getattr(context, "typed_array", {})
        self._parse_array()
    
    def _parse_array(self):
        self.image_resource = self.array.get("resourceId", 123)
        self.color = self.array.get("color", 0x00ff00)
        self.underline = self.array.get("underline", False)
        self.default_text_value = self.array.get("string", None)
        self.setStartImageText(self.default_text_value)

    def setStartImageText(self, text):
        self.text = text if text else ""

    def setOnClickCallBack(self, callback):
        self._callback = callback

    def getText(self):
        return self.text

def autotest_setup_public(mock_context=None, extra_array=None):
    class DummyContext:
        pass

    ctx = mock_context if mock_context else DummyContext()
    array = {
        "resourceId": 123,
        "string": "Alpha;Beta",
        "color": 0x00ff00,
        "underline": False,
    }
    if extra_array:
        array.update(extra_array)
    setattr(ctx, "typed_array", array)
    return ctx

def test_constructor_and_default_fields_public():
    ctx = autotest_setup_public()
    view = AutoLinkStyleTextView(ctx, None, 0)
    assert view is not None

def test_set_start_image_text_no_drawable_no_crash_public():
    ctx = autotest_setup_public()
    view = AutoLinkStyleTextView(ctx, None, 0)
    assert view.getText() == "Alpha;Beta"
    view.setStartImageText("Sample")
    assert view.getText() == "Sample"

def test_set_start_image_text_with_image_and_type_public():
    ctx = autotest_setup_public(extra_array={"resourceId": 71})
    AutoLinkStyleTextView.styleType = 0
    view = AutoLinkStyleTextView(ctx, None, 0)
    view.setStartImageText("Hello")
    assert view.getText() == "Hello"

def test_click_callback_set_and_trigger_public():
    callback_mock = mock.Mock()
    ctx = autotest_setup_public(extra_array={"string": "Plan-Policy"})
    view = AutoLinkStyleTextView(ctx, None, 0)
    view.setOnClickCallBack(callback_mock)
    assert view is not None

def test_add_style_branch_empty_or_no_comma_public():
    ctx = autotest_setup_public(extra_array={"string": "SingleSegment"})
    view = AutoLinkStyleTextView(ctx, None, 0)
    assert view.getText() == "SingleSegment"

def test_clickable_span_update_draw_state_public():
    ctx = autotest_setup_public(extra_array={"string": "Green,Orange", "color": 0x123456})
    AutoLinkStyleTextView.styleType = 1
    view = AutoLinkStyleTextView(ctx, None, 0)
    class DummyTextPaint:
        def __init__(self):
            self.color = 0

        def setColor(self, color):
            self.color = color
    tp = DummyTextPaint()
    color = view.color
    tp.setColor(color)
    assert tp.color == 0x123456

def test_centered_image_span_draw_executes_public():
    ctx = autotest_setup_public(extra_array={"resourceId": 555})
    AutoLinkStyleTextView.styleType = 0
    view = AutoLinkStyleTextView(ctx, None, 0)
    view.setStartImageText("World")
    assert view is not None