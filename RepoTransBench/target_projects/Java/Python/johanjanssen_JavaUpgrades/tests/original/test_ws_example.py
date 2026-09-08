import pytest

class WSExample:
    @staticmethod
    def main(args):
        pass

def test_main_no_exceptions():
    WSExample.main([])