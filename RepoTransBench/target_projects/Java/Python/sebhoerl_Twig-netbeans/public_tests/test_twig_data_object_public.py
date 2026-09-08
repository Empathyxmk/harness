import pytest

class TwigDataObject:
    def __init__(self, filename):
        self.filename = filename
    def getFileExtension(self):
        return self.filename.split('.')[-1]
    def isTwigFile(self):
        return self.filename.endswith('.twig')

def test_twig_data_object_extension_public():
    obj = TwigDataObject("examplePublic.twig")
    assert obj.getFileExtension() == "twig"

def test_is_twig_file_returns_true_public():
    obj = TwigDataObject("anotherfilePublic.twig")
    assert obj.isTwigFile()