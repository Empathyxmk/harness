import pytest

class ShopApplication:
    @staticmethod
    def main(args):
        pass

def test_main_runs_without_exception():
    ShopApplication.main([])