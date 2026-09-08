import pytest
from src.spring5webapp.sample_branching_service import SampleBranchingService

class TestSampleBranchingServicePublic:
    def setup_method(self):
        self.service = SampleBranchingService()
    
    def test_categorize_negative_public(self):
        assert self.service.categorize_number(-15) == "negative"

    def test_categorize_zero_public(self):
        assert self.service.categorize_number(0) == "zero"
    
    def test_categorize_small_public(self):
        assert self.service.categorize_number(8) == "small"
    
    def test_categorize_large_public(self):
        assert self.service.categorize_number(50) == "large"

    def test_is_even_true_public(self):
        assert self.service.is_even(6) is True

    def test_is_even_false_public(self):
        assert self.service.is_even(9) is False