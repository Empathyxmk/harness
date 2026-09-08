import pytest

from tests.original.test_round_status_impl import RoundStatusImpl

def test_builder_chain():
    builder = RoundStatusImpl.RoundStatusBuilder()
    builder.setMRadius(9.0) \
           .setMTopLeftRadius(8.0) \
           .setMTopRightRadius(7.0) \
           .setMBottomLeftRadius(6.0) \
           .setMBottomRightRadius(5.0)

    impl = builder.build()
    assert impl.getRadius() == pytest.approx(9.0, abs=1e-6)
    assert impl.getTopLeftRadius() == pytest.approx(8.0, abs=1e-6)
    assert impl.getTopRightRadius() == pytest.approx(7.0, abs=1e-6)
    assert impl.getBottomLeftRadius() == pytest.approx(6.0, abs=1e-6)
    assert impl.getBottomRightRadius() == pytest.approx(5.0, abs=1e-6)