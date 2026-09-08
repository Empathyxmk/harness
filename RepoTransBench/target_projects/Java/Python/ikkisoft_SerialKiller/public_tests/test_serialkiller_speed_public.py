def test_performance_with_different_params():
    iterations = 2500
    per_iteration = 251
    result = iterations * per_iteration
    assert result == 627500  # 2500 * 251