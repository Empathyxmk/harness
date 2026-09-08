import pytest
from unittest.mock import MagicMock
from types import SimpleNamespace

# Since we do not have access to the full React implementation in Python,
# we'll simulate the lifecycle method testing logic and spy calls.

class CompositeComponent:
    def __init__(self, spyForComponentWillMount, spyForComponentWillUnmount):
        self.props = SimpleNamespace(
            spyForComponentWillMount=spyForComponentWillMount,
            spyForComponentWillUnmount=spyForComponentWillUnmount
        )
        self.componentWillMount()
        # componentWillUnmount would be called manually if needed

    def componentWillMount(self):
        self.props.spyForComponentWillMount()

    def componentWillUnmount(self):
        self.props.spyForComponentWillUnmount()

    def render(self):
        return "CompositeComponent"

def renderToString(component):
    # Simulate the server-side rendering call
    return component.render()

def test_render_to_string_calls_component_will_mount():
    spy_mount = MagicMock()
    spy_unmount = lambda: None
    _ = renderToString(
        CompositeComponent(spy_mount, spy_unmount)
    )
    assert spy_mount.call_count == 1, "#componentWillMount() has been called once"

def test_render_to_string_does_not_call_component_will_unmount():
    spy_mount = lambda: None
    spy_unmount = MagicMock()
    _ = renderToString(
        CompositeComponent(spy_mount, spy_unmount)
    )
    assert spy_unmount.call_count == 0, "#componentWillUnmount() has not been called"