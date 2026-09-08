import pytest
from easy_thumbnails.fields import ThumbnailerField

class DummyFile:
    def __init__(self, name):
        self.name = name

def test_thumbnailerfield_deconstruct_public():
    field = ThumbnailerField(upload_to='gallery/images/')
    name, path, args, kwargs = field.deconstruct()
    assert name == 'ThumbnailerField'
    assert kwargs['upload_to'] == 'gallery/images/'

def test_thumbnailerfield_generate_thumbnail_public():
    field = ThumbnailerField()
    file = DummyFile('test_img2.jpg')
    # Just check that resolve_generate_filename produces different names
    out1 = field.generate_filename(file, 'foo1.jpg')
    out2 = field.generate_filename(file, 'foo2.jpg')
    assert out1 != out2