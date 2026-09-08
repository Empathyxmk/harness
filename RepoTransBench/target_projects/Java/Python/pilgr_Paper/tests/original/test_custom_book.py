import pytest

class DummyBook(dict):
    def write(self, key, value):
        self[key] = value
    def read(self, key, default=None):
        if key in self:
            return self[key]
        return default
    def destroy(self):
        self.clear()
    def contains(self, key):
        return key in self
    def delete(self, key):
        self.pop(key, None)
    def getPath(self, key=None):
        if key:
            return f"/io.paperdb.test/files/custom/{key}.pt"
        return "/io.paperdb.test/files/custom"

class DummyPaper:
    _books = {}
    @classmethod
    def init(cls, ctx=None):
        cls._books = {"": DummyBook(), "custom": DummyBook()}
    @classmethod
    def book(cls, name=""):
        if name not in cls._books:
            cls._books[name] = DummyBook()
        return cls._books[name]

@pytest.fixture(autouse=True)
def setup():
    DummyPaper.init()
    yield

def test_get_folder_path_for_book_custom():
    path = DummyPaper.book("custom").getPath()
    assert path.endswith("/io.paperdb.test/files/custom")

def test_get_file_path_for_key_custom_book():
    path = DummyPaper.book("custom").getPath("my_key")
    assert path.endswith("/io.paperdb.test/files/custom/my_key.pt")

def test_read_write_delete_to_different_books():
    custom = "custom"
    DummyPaper.book().destroy()
    DummyPaper.book(custom).destroy()
    DummyPaper.book().write("city", "Victoria")
    DummyPaper.book(custom).write("city", "Kyiv")
    assert DummyPaper.book().read("city") == "Victoria"
    assert DummyPaper.book(custom).read("city") == "Kyiv"
    DummyPaper.book().delete("city")
    assert not DummyPaper.book().contains("city")
    assert DummyPaper.book(custom).contains("city")