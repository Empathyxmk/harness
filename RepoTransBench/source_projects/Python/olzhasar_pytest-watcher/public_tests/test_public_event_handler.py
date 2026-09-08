from pytest_watcher.event_handler import EventHandler

def test_event_handler_modified(tmp_path):
    changed = []
    class DummyHandler(EventHandler):
        def on_modified(self, event):
            changed.append("modified")

    handler = DummyHandler()
    # simulate a minimal event object
    event = type("Event", (), {"src_path": str(tmp_path / "afile.txt")})
    handler.on_modified(event)
    assert "modified" in changed