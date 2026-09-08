from src.fitchart.fake_classes import AnimationMode, Renderer, FitChartValue

def test_fake_classes_exist_public():
    fc = FitChartValue(42, 0x123)
    assert fc.getValue() == 42
    assert fc.getColor() == 0x123
    fc.setStartAngle(33)
    assert fc.getStartAngle() == 33
    fc.setSweepAngle(77)
    assert fc.getSweepAngle() == 77
    fc.setPaint("paint_pub")
    assert fc.getPaint() == "paint_pub"

    assert AnimationMode.LINEAR.name == "LINEAR"
    assert AnimationMode.OVERDRAW.name == "OVERDRAW"