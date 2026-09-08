import types
import overholt.tasks

def test_send_manager_added_email_prints(monkeypatch, capsys):
    # Patch celery so as not to run tasks asynchronously
    func = overholt.tasks.send_manager_added_email
    func("user1@example.com", "user2@example.com")
    out, _ = capsys.readouterr()
    assert "sending manager added email" in out

def test_send_manager_removed_email_prints(monkeypatch, capsys):
    func = overholt.tasks.send_manager_removed_email
    func("user3@example.com")
    out, _ = capsys.readouterr()
    assert "sending manager removed email" in out