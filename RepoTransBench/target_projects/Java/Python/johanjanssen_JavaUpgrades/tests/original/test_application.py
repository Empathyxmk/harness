import pytest

class Application:
    @staticmethod
    def main(args):
        pass # Does not throw exception

def test_main_runs_without_exception():
    Application.main([])