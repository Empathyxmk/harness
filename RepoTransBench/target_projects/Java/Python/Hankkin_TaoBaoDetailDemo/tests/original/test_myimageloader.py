import unittest

class MyImageLoader:
    _instance = None  # Singleton storage

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyImageLoader, cls).__new__(cls)
        return cls._instance

    @classmethod
    def getInstance(cls):
        return cls()

    # Dummy display methods
    def displayImage(self, context, source, image_view, *args):
        # Accept all variants
        pass

    def displayImageFitCenter(self, context, source, image_view, *args):
        pass

    def displayImageCen(self, context, source, image_view, *args):
        pass

class TestMyImageLoader(unittest.TestCase):

    def test_get_instance_singleton(self):
        loader1 = MyImageLoader.getInstance()
        loader2 = MyImageLoader.getInstance()
        self.assertIs(loader1, loader2)

    def test_display_image_signatures(self):
        context = object()
        loader = MyImageLoader.getInstance()
        image_view = object()
        progress_bar = object()

        loader.displayImage(context, "http://example.com/img.png", image_view)
        loader.displayImage(context, "http://example.com/img2.png", image_view, progress_bar)
        loader.displayImage(context, object(), image_view)
        loader.displayImage(context, object(), image_view, 100, 100)
        loader.displayImage(context, "http://example.com/img3.png", image_view, 100, 100, progress_bar)
        loader.displayImage(context, "http://example.com/img4.png", image_view, 120, 80)
        loader.displayImageFitCenter(context, "http://example.com/img5.png", image_view, 80, 90)
        loader.displayImageCen(context, "http://example.com/img6.png", image_view, 40, 20)