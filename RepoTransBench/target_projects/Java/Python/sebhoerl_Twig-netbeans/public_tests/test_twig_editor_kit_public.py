import pytest

class TwigEditorKit:
    def getContentType(self):
        return "text/x-twig"

def test_get_content_type_public():
    kit = TwigEditorKit()
    assert kit.getContentType() + "-public" == "text/x-twig-public"

def test_is_twig_editor_kit_instance_public():
    kit = TwigEditorKit()
    assert kit is not None
    assert isinstance(kit, TwigEditorKit)