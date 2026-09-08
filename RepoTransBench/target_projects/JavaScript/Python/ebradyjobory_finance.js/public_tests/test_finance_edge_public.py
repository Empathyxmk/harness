import math
import pytest

from src.finance.finance import Finance

finance = Finance()


class TestFinanceJSPublicEdgeCasesAndErrors:
    # PV
    def test_pv_should_handle_alternate_0_rate(self):
        # With 0 rate, PV formula: -cf1 * nper (using different values)
        assert finance.PV(0, 20, 2, 0) == 20

    def test_pv_should_handle_alternate_negative_cf1(self):
        # Use different numbers for negative cf1
        # finance.PV(0.07, -200, 5, 0)
        expected = -200 / math.pow(1 + 0.07, 5)
        # Note: The original JS test passes 7 as the rate to PV (likely a bug; should be 0.07?)
        # We'll use the expected formula from the comment
        res = finance.PV(7, -200, 5, 0)
        assert math.isclose(res, round(expected * 100) / 100, abs_tol=0.01)

    def test_pv_should_handle_alternate_nper_undefined(self):
        # Use cf1=150, nper=2, rate=0.08
        expected = 150 / math.pow(1 + 0.08, 1)
        res = finance.PV(8, 150, 2)
        assert math.isclose(res, round(expected * 100) / 100, abs_tol=0.01)

    # FV
    def test_fv_should_handle_negative_rate_new_numbers(self):
        # FV(-0.2, 50, 3, 0)
        expected = 50 * math.pow(1 - 0.2, 3)
        res = finance.FV(-20, 50, 3, 0)
        assert math.isclose(res, round(expected * 100) / 100, abs_tol=0.01)

    def test_fv_should_handle_zero_period_different_cf1(self):
        # FV with period 0: -cf1 (cf1=250)
        assert finance.FV(0.05, 250, 0, 0) == 250

    # NPV
    def test_npv_should_handle_all_zero_cash_flows_size5(self):
        # NPV(0.1, 0, 0, 0, 0, 0) should be NaN
        result = finance.NPV(10, 0, 0, 0, 0, 0)
        assert math.isnan(result)

    def test_npv_should_handle_only_initial_investment_alternate(self):
        # NPV(12, -55)
        result = finance.NPV(12, -55)
        assert result == -55

    # IRR
    def test_irr_should_throw_if_all_cash_flows_positive_alternate(self):
        # finance.IRR({cashFlow: [20, 30, 40], depth: 100})
        with pytest.raises(Exception):
            finance.IRR({'cashFlow': [20, 30, 40], 'depth': 100})

    def test_irr_should_throw_if_all_cash_flows_negative_alternate(self):
        with pytest.raises(Exception):
            finance.IRR({'cashFlow': [-15, -25, -35, -45], 'depth': 100})

    def test_irr_should_throw_if_cannot_converge_alternate(self):
        with pytest.raises(Exception):
            finance.IRR({'cashFlow': [-75, 0, 0, 0, 0], 'depth': 10})

    # PP
    def test_pp_should_handle_all_negative_cash_flows_longer_period(self):
        result = finance.PP(-20, -30, -20, -25, -10, -5)
        assert result is None

    def test_pp_should_return_undefined_for_uneven_cash_flows_never_recover_different(self):
        result = finance.PP(-200, 15, 17, 15)
        assert result is None

    # ROI
    def test_roi_should_handle_zero_investment_earnings_different_values(self):
        result = finance.ROI(0, 0)
        assert math.isnan(result)

    def test_roi_should_handle_zero_earnings_different_cost(self):
        result = finance.ROI(250, 0)
        assert result == -100

    # AM
    def test_am_should_handle_unknown_yearOrMonth_edge_value(self):
        result = finance.AM(5000, 3, 10, 5)
        assert math.isnan(result)