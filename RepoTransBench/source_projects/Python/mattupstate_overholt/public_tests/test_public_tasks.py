import overholt.tasks

def test_public_send_manager_added_email_content(capsys):
    # Use different emails than existing test
    func = overholt.tasks.send_manager_added_email
    func("public1@example.com", "public2@example.com")
    out, _ = capsys.readouterr()
    assert "manager added email" in out  # Shorter substring, different test but same check

def test_public_send_manager_removed_email_content(capsys):
    func = overholt.tasks.send_manager_removed_email
    func("public3@example.com")
    out, _ = capsys.readouterr()
    assert "manager removed email" in out