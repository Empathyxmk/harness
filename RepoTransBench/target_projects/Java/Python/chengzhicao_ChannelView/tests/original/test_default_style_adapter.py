class DefaultViewHolder:
    def __init__(self, item_view):
        self.item_view = item_view

class DefaultStyleAdapter:
    def __init__(self):
        # Store style configuration for test
        self._channel_normal_text_color = None
        self._channel_normal_background = None
        self._channel_fixed_text_color = None
        self._channel_fixed_background = None
        self._channel_edit_background = None
        self._channel_focused_background = None
        self._channel_focused_text_color = None
        self._channel_text_size = None

    def create_style_view(self, parent, channel_name):
        # In Android, creates a View/TextView; in Python, simulate via dict
        item = {"type": "textview", "text": channel_name, "color": None, "size": None, "bg": None}
        holder = DefaultViewHolder(item)
        return holder

    def set_text_color(self, view, color):
        view["color"] = color

    def set_text_size(self, view, size):
        view["size"] = float(size)

    def set_background_resource(self, view, res):
        view["bg"] = res

    # Style config setters
    def set_channel_normal_text_color(self, v):
        self._channel_normal_text_color = v
    def set_channel_normal_background(self, v):
        self._channel_normal_background = v
    def set_channel_fixed_text_color(self, v):
        self._channel_fixed_text_color = v
    def set_channel_fixed_background(self, v):
        self._channel_fixed_background = v
    def set_channel_edit_background(self, v):
        self._channel_edit_background = v
    def set_channel_focused_background(self, v):
        self._channel_focused_background = v
    def set_channel_focused_text_color(self, v):
        self._channel_focused_text_color = v
    def set_channel_text_size(self, v):
        self._channel_text_size = v

    # Simulate style methods
    def set_normal_style(self, holder):
        # would set colors & backgrounds; for Python, "touches" simulated values
        pass
    def set_fixed_style(self, holder):
        pass
    def set_edit_style(self, holder):
        pass
    def set_focused_style(self, holder):
        pass

class TestAdapter(DefaultStyleAdapter):
    def __init__(self):
        super().__init__()
        self.parent = None

    def create_style_view(self, parent, channel_name):
        self.parent = parent
        return super().create_style_view(parent, channel_name)

class TestViewGroup(dict):
    def __init__(self, context):
        super().__init__()
        self["context"] = context

class MockContext:
    pass

def test_create_style_view():
    adapter = TestAdapter()
    mock_context = MockContext()
    parent = TestViewGroup(mock_context)
    holder = adapter.create_style_view(parent, "MyChannel")
    assert holder.item_view["type"] == "textview"
    assert holder.item_view["text"] == "MyChannel"

def test_setters():
    adapter = TestAdapter()
    mock_context = MockContext()
    view = {"type": "textview", "color": None, "size": None, "bg": None}
    # set_text_color
    adapter.set_text_color(view, 0xff112233)
    assert view["color"] == 0xff112233

    # set_text_size
    adapter.set_text_size(view, 18)
    assert view["size"] == 18.0

    # set_background_resource (should set without error)
    adapter.set_background_resource(view, 0)
    assert view["bg"] == 0

def test_set_style_methods():
    adapter = TestAdapter()
    mock_context = MockContext()
    view = {"type": "textview", "color": None, "size": None, "bg": None}
    holder = DefaultViewHolder(view)
    adapter.set_channel_normal_text_color(0xf1)
    adapter.set_channel_normal_background(0xa1)
    adapter.set_channel_fixed_text_color(0xf2)
    adapter.set_channel_fixed_background(0xa2)
    adapter.set_channel_edit_background(0xa3)
    adapter.set_channel_focused_background(0xa4)
    adapter.set_channel_focused_text_color(0xf3)

    # Should not throw or fail
    adapter.set_normal_style(holder)
    adapter.set_fixed_style(holder)
    adapter.set_edit_style(holder)
    adapter.set_focused_style(holder)

def test_set_channel_text_size():
    adapter = TestAdapter()
    adapter.set_channel_text_size(123)
    assert adapter._channel_text_size == 123