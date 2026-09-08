import pytest
from forms_builder.forms import utils

def test_is_file_extensions():
    assert utils.is_file("photo.PNG")
    assert utils.is_file("document.PDF")
    assert not utils.is_file("example.txt")
    assert not utils.is_file("no_dot")

def test_slugify_basic():
    s = " Hello__World__ "
    sl = utils.slugify(s)
    assert sl == "hello-world"

def test_is_email_cases():
    assert utils.is_email("foo@bar.com")
    assert not utils.is_email("notanemail")
    assert not utils.is_email("@nodomain")

def test_content_as_txt_html():
    # Just check no exceptions, return str
    class Dummy:
        class _meta:
            app_label = "a"
            model_name = "b"
    text = utils.content_as_text(Dummy())
    html = utils.content_as_html(Dummy())
    assert isinstance(text, str)
    assert isinstance(html, str)

def test_get_admin_url_format():
    class Dummy:
        _meta = type("Meta", (), {"app_label": "myapp", "model_name": "dummy"})
        pk = 1
    url = utils.get_admin_url(Dummy())
    assert "myapp/dummy/1/" in url or "myapp/dummy/1" in url