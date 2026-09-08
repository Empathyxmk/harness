# Just verifies fake classes importable (no test logic needed; used for code compatibility in tests)
from src.fitchart.fake_classes import AnimationMode, Renderer, FitChartValue

def test_fake_classes_exist():
    fc = FitChartValue(1, 2)
    assert fc.getValue() == 1
    assert fc.getColor() == 2
    fc.setStartAngle(10)
    assert fc.getStartAngle() == 10
    fc.setSweepAngle(20)
    assert fc.getSweepAngle() == 20
    fc.setPaint("paint_obj")
    assert fc.getPaint() == "paint_obj"

    assert AnimationMode.LINEAR.name == "LINEAR"
    assert AnimationMode.OVERDRAW.name == "OVERDRAW"