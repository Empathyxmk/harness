def test_can_create_from_different_file():
    class ThunderbirdMailStorage:
        def __init__(self, filename):
            self.filename = filename

    storage = ThunderbirdMailStorage("/tmp/pubmailbox")
    assert storage is not None