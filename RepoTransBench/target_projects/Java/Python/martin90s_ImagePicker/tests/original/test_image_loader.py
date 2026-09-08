import pytest

class ImageView:
    def __init__(self, ctx=None):
        self._tag = None
    def set_tag(self, tag):
        self._tag = tag
    def get_tag(self):
        return self._tag

class ImageLoader:
    def bind_image(self, image_view, uri, width=None, height=None):
        raise NotImplementedError
    def create_image_view(self, context):
        raise NotImplementedError
    def create_fake_image_view(self, context):
        raise NotImplementedError

class DummyImageLoader(ImageLoader):
    def bind_image(self, image_view, uri, width=None, height=None):
        if image_view is not None and uri is not None:
            if width is not None and height is not None:
                image_view.set_tag(f"{uri}{width}{height}")
            else:
                image_view.set_tag(f"{uri}")

    def create_image_view(self, context):
        return ImageView(context)

    def create_fake_image_view(self, context):
        return ImageView(context)

def test_image_loader_basic():
    loader = DummyImageLoader()
    ctx = object()
    image = ImageView(ctx)
    uri = "file://x.png"
    loader.bind_image(image, uri, 100, 200)
    assert isinstance(image.get_tag(), str)
    loader.bind_image(image, uri)
    assert isinstance(image.get_tag(), str)
    iv1 = loader.create_image_view(ctx)
    assert iv1 is not None
    iv2 = loader.create_fake_image_view(ctx)
    assert iv2 is not None