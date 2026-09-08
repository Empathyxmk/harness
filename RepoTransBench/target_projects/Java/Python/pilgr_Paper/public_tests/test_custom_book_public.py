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
            return f"/io.paperdb.test/files/public_custom/{key}.pt"
        return "/io.paperdb.test/files/public_custom"

class DummyPaper:
    _books = {}
    @classmethod
    def init(cls, ctx=None):
        cls._books = {"": DummyBook(), "public_custom": DummyBook()}
    @classmethod
    def book(cls, name=""):
        if name not in cls._books:
            cls._books[name] = DummyBook()
        return cls._books[name]

@pytest.fixture(autouse=True)
def setup():
    DummyPaper.init()
    yield

def test_get_folder_path_for_book_custom_public():
    path = DummyPaper.book("public_custom").getPath()
    assert path.endswith("/io.paperdb.test/files/public_custom")

def test_get_file_path_for_key_custom_book_public():
    path = DummyPaper.book("public_custom").getPath("my_val")
    assert path.endswith("/io.paperdb.test/files/public_custom/my_val.pt")

def test_read_write_delete_to_different_books_public():
    public_book = "public_custom"
    DummyPaper.book().destroy()
    DummyPaper.book(public_book).destroy()
    DummyPaper.book().write("country", "Denmark")
    DummyPaper.book(public_book).write("country", "Norway")
    assert DummyPaper.book().read("country") == "Denmark"
    assert DummyPaper.book(public_book).read("country") == "Norway"
    DummyPaper.book().delete("country")
    assert not DummyPaper.book().contains("country")
    assert DummyPaper.book(public_book).contains("country")