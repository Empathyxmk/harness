import pytest
from src.spring5webapp.sample_branching_service import SampleBranchingService

class TestSampleBranchingService:
    def setup_method(self):
        self.service = SampleBranchingService()
    
    def test_categorize_negative(self):
        assert self.service.categorize_number(-5) == "negative"

    def test_categorize_zero(self):
        assert self.service.categorize_number(0) == "zero"
    
    def test_categorize_small(self):
        assert self.service.categorize_number(5) == "small"
    
    def test_categorize_large(self):
        assert self.service.categorize_number(100) == "large"

    def test_is_even_true(self):
        assert self.service.is_even(2) is True

    def test_is_even_false(self):
        assert self.service.is_even(3) is False