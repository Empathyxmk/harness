import pytest

class Application:
    @staticmethod
    def main(args):
        pass

def test_main_runs_without_exception_public():
    Application.main([])