import pytest
import io
from mammoth import images

class DummyImage:
    def __init__(self, content_type="foo/bar", data=b"bytes", alt_text=None):
        self.content_type = content_type
        self._data = data
        self.alt_text = alt_text
    def open(self):
        return io.BytesIO(self._data)

def test_img_element_adds_alt():
    def src_func(image):
        return {"src": "mine"}
    converter = images.img_element(src_func)
    img = DummyImage(alt_text="alt text here")
    el = converter(img)
    assert isinstance(el, list) and el[0].tag == "img"
    assert el[0].attributes["src"] == "mine"
    assert el[0].attributes["alt"] == "alt text here"

def test_img_element_no_alt():
    def src_func(image):
        return {"src": "test"}
    converter = images.img_element(src_func)
    img = DummyImage(alt_text=None)
    el = converter(img)
    assert "alt" not in el[0].attributes

def test_data_uri_encodes_base64(monkeypatch):
    fake_data = b"imgbytes"
    img = DummyImage(content_type="image/png", data=fake_data)
    out = images.data_uri(img)
    assert out[0].tag == "img"
    assert out[0].attributes["src"].startswith("data:image/png;base64,")

def test_inline_alias_works():
    def _fake_func(image):
        return {"src": "abc"}
    inline = images.inline(_fake_func)
    img = DummyImage()
    el = inline(img)
    assert isinstance(el, list)