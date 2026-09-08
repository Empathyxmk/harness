import pytest
from easy_thumbnails.templatetags import thumbnail

def test_thumbnailer_filter_render_public():
    # Basic test for the filter function to render a thumbnail tag
    class DummyImgObj:
        url = 'abc.jpg'
    rv = thumbnail.thumbnailer_filter(DummyImgObj(), '150x75')
    assert '150x75' in rv

def test_thumbnail_tag_imgpath_public():
    out = thumbnail.thumbnail_tag('xyz.jpg', '60x90')
    assert 'xyz.jpg' in out and '60x90' in out