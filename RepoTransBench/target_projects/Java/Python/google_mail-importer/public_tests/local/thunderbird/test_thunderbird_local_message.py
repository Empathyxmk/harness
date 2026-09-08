def test_different_message_id_default_folder():
    class ThunderbirdLocalMessage:
        def __init__(self, message_id, folder):
            self.message_id = message_id
            self.folders = [folder]

        def getMessageId(self):
            return self.message_id

        def getFolders(self):
            return self.folders

    msg = ThunderbirdLocalMessage("xyz789", "public_folder")
    assert msg.getMessageId() == "xyz789"
    assert "public_folder" in msg.getFolders()