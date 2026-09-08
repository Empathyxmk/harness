import pytest

class AnnotationExample:
    def is_annotated(self):
        return True

def test_annotation_message_public():
    example = AnnotationExample()
    assert example.is_annotated()