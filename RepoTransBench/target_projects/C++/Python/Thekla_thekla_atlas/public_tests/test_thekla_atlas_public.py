# Translation of: src/thekla/thekla_atlas_public_test.cpp

import pytest
from src.thekla_atlas_dummy import Atlas

def test_different_parameter():
    atlas = Atlas()

    desired_chart_count = 7
    atlas.setDesiredChartCount(desired_chart_count)
    lambda_init = 0.15
    atlas.setInitLambdaCharts(lambda_init)
    assert atlas.getDesiredChartCount() == desired_chart_count
    assert atlas.getInitLambdaCharts() == pytest.approx(lambda_init)

    # Set other, differently-valued params and verify
    atlas.setSomeParameter(2.718)
    assert atlas.getSomeParameter() == pytest.approx(2.718)

def test_fail_safe_with_invalid_value():
    atlas = Atlas()
    atlas.setDesiredChartCount(-2)
    assert atlas.getDesiredChartCount() != 10
    atlas.setInitLambdaCharts(5.0)
    assert atlas.getInitLambdaCharts() == pytest.approx(5.0)