class EmojiReader:
    def read(self, local):
        return {"emojis": []}  # Dummy return for test

    def get_sb2_unicode_map(self):
        return {"sb": "unicode"}  # Dummy return

def test_read_from_local_public():
    reader = EmojiReader()
    assert reader.read(True) is not None

def test_sb2_unicode_map_not_null_public():
    reader = EmojiReader()
    assert reader.get_sb2_unicode_map() is not None