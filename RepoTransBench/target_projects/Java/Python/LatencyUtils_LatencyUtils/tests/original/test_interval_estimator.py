import pytest

class IntervalEstimator:
    def record_interval(self, when):
        raise NotImplementedError

    def get_estimated_interval(self, when):
        raise NotImplementedError

def test_abstract_method_throws():
    class DummyEstimator(IntervalEstimator):
        def record_interval(self, when):
            pass
        def get_estimated_interval(self, when):
            return 123
    estimator = DummyEstimator()
    estimator.record_interval(1)
    est = estimator.get_estimated_interval(2)
    assert est == 123