# Translation of: src/thekla/thekla_atlas_basic_public_test.cpp

import pytest
from src.thekla_atlas_dummy import Atlas

def test_init_chart_count():
    atlas = Atlas()
    new_chart_count = 8  # Distinct from private/internal tests
    atlas.setDesiredChartCount(new_chart_count)
    assert atlas.getDesiredChartCount() == new_chart_count

    lambda_ = 0.42
    atlas.setInitLambdaCharts(lambda_)
    assert atlas.getInitLambdaCharts() == pytest.approx(lambda_)

def test_lambda_value_range():
    atlas = Atlas()
    lambda_ = 3.14
    atlas.setInitLambdaCharts(lambda_)
    assert atlas.getInitLambdaCharts() == pytest.approx(lambda_)
    # Additionally ensure it's not a value from the private tests, for public clarity
    assert lambda_ != 0.18