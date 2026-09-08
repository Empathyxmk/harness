def test_abstract_method_returns_different_value():
    class IntervalEstimator:
        def record_interval(self, when):
            pass
        def get_estimated_interval(self, when):
            return 456
    estimator = IntervalEstimator()
    estimator.record_interval(100)
    est = estimator.get_estimated_interval(101)
    assert est == 456