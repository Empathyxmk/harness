import pytest

class ImageLoader:
    def display(self, context, path, image_view, width, height):
        raise NotImplementedError
    def pause(self, context):
        raise NotImplementedError
    def resume(self, context):
        raise NotImplementedError
    def clear_memory_cache(self, context):
        raise NotImplementedError
    def clear_disk_cache(self, context):
        raise NotImplementedError

class DummyImageLoader(ImageLoader):
    def __init__(self):
        self.display_called = False
        self.pause_called = False
        self.resume_called = False
        self.clear_mem_called = False
        self.clear_disk_called = False

    def display(self, context, path, image_view, width, height):
        self.display_called = True

    def pause(self, context):
        self.pause_called = True

    def resume(self, context):
        self.resume_called = True

    def clear_memory_cache(self, context):
        self.clear_mem_called = True

    def clear_disk_cache(self, context):
        self.clear_disk_called = True

def test_display_method_public():
    loader = DummyImageLoader()
    loader.display(None, "some/path/public", None, 301, 401)
    assert loader.display_called

def test_pause_and_resume_and_clear_caches_public():
    loader = DummyImageLoader()
    loader.pause(None)
    assert loader.pause_called
    loader.resume(None)
    assert loader.resume_called
    loader.clear_memory_cache(None)
    assert loader.clear_mem_called
    loader.clear_disk_cache(None)
    assert loader.clear_disk_called