import math
import pytest

from src.finance.finance import Finance

finance = Finance()


class TestFinanceJSEdgeCasesAndErrors:
    # PV
    def test_pv_should_handle_0_rate(self):
        # With 0 rate, PV formula: -cf1 * nper
        assert finance.PV(0, 10, 1, 0) == 10

    def test_pv_should_handle_negative_cf1(self):
        # finance.PV(0.05, -100, 10, 0) = -99.5
        result = finance.PV(0.05, -100, 10, 0)
        assert math.isclose(result, -99.5, abs_tol=0.01)

    def test_pv_should_handle_nper_undefined(self):
        # finance.PV(0.05, 100, 10) = 99.5
        result = finance.PV(0.05, 100, 10)
        assert math.isclose(result, 99.5, abs_tol=0.01)

    # FV
    def test_fv_should_handle_negative_rate(self):
        # finance.FV(-0.1, 100, 2, 0) = 99.8
        result = finance.FV(-0.1, 100, 2, 0)
        assert math.isclose(result, 99.8, abs_tol=0.01)

    def test_fv_should_handle_zero_period(self):
        # FV with period 0: -cf1 (same as implementation)
        assert finance.FV(0.1, 100, 0, 0) == 100

    # NPV
    def test_npv_should_handle_all_zero_cash_flows(self):
        # finance.NPV(0.05, [0,0,0]) returns NaN
        result = finance.NPV(0.05, [0, 0, 0])
        assert math.isnan(result)

    def test_npv_should_handle_only_initial_investment(self):
        result = finance.NPV(0.05, [-100])
        assert result == -100

    # IRR
    def test_irr_should_throw_if_all_cash_flows_positive(self):
        with pytest.raises(Exception):
            finance.IRR([10, 10, 10])

    def test_irr_should_throw_if_all_cash_flows_negative(self):
        with pytest.raises(Exception):
            finance.IRR([-10, -20, -30])

    def test_irr_should_throw_if_cannot_converge(self):
        with pytest.raises(Exception):
            finance.IRR([-100, 0, 0, 0])

    # PP
    def test_pp_should_handle_even_cash_flows_with_negative_values(self):
        result = finance.PP([-10, -10, -10])
        assert result is None  # JS .be.undefined = Python None

    def test_pp_should_return_undefined_for_uneven_cash_flows_that_never_recover(self):
        result = finance.PP([-100, 10, 10, 10])
        assert result is None

    # ROI
    def test_roi_should_handle_zero_investment(self):
        result = finance.ROI(0, 0)
        assert math.isnan(result)

    def test_roi_should_handle_zero_earnings(self):
        result = finance.ROI(100, 0)
        assert result == -100

    # AM
    def test_am_should_handle_unknown_yearOrMonth(self):
        result = finance.AM(1000, 5, 10, 3)
        assert math.isnan(result)