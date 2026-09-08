package original

import (
	"fitchart"
	"testing"
)

func TestLinearValueRenderer_BuildPath_StartAngleLessThanSeek_BuildsArc(t *testing.T) {
	area := fitchart.RectF{0, 0, 100, 100}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(0)
	value.SetSweepAngle(100)
	renderer := fitchart.NewLinearValueRenderer(area, value)

	path := renderer.BuildPath(0.5, 50)

	if path == nil {
		t.Errorf("Expected path to be non-nil when startAngle <= animationSeek")
	}
}

func TestLinearValueRenderer_BuildPath_StartAngleGreaterThanSeek_ReturnsNil(t *testing.T) {
	area := fitchart.RectF{0, 0, 100, 100}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(100)
	value.SetSweepAngle(50)
	renderer := fitchart.NewLinearValueRenderer(area, value)

	path := renderer.BuildPath(0.5, 40)

	if path != nil {
		t.Errorf("Expected path to be nil when startAngle > animationSeek")
	}
}

func TestLinearValueRenderer_CalculateSweepAngle_PathBranches(t *testing.T) {
	area := fitchart.RectF{0, 0, 100, 100}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(20)
	value.SetSweepAngle(50)
	renderer := fitchart.NewLinearValueRenderer(area, value)

	// force totalSizeOfValue > animationSeek
	_ = renderer.BuildPath(0.5, 40)
	// force totalSizeOfValue <= animationSeek
	_ = renderer.BuildPath(0.5, 80)
	// Just test that above calls do not panic.
}