import pytest

class TestHamcrestList:
    def setup_method(self, method):
        self.customers_names = ["John", "Michael", "Edwin"]

    def test_list_without_hamcrest(self):
        assert "John" in self.customers_names or "Michael" in self.customers_names or "Edwin" in self.customers_names

    def test_list_with_hamcrest(self):
        # Mimic Hamcrest's hasItems using Python's all()
        for name in ["John", "Michael", "Edwin"]:
            assert name in self.customers_names