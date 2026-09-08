import pytest

class AnnotationExample:
    @staticmethod
    def main(args):
        # run, no error
        pass

def test_main_no_exceptions():
    AnnotationExample.main([])