package public_tests

import (
	"fitchart"
	"testing"
)

func TestLinearValueRendererPublic_BuildPath_DifferentStartAngleLessThanSeek_BuildsArc(t *testing.T) {
	area := fitchart.RectF{5, 5, 120, 120}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(10)
	value.SetSweepAngle(30)
	renderer := fitchart.NewLinearValueRenderer(area, value)

	path := renderer.BuildPath(0.7, 25)
	if path == nil {
		t.Errorf("Expected path to be non-nil when startAngle <= animationSeek")
	}
}

func TestLinearValueRendererPublic_BuildPath_DifferentStartAngleGreaterThanSeek_ReturnsNil(t *testing.T) {
	area := fitchart.RectF{10, 10, 80, 80}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(60)
	value.SetSweepAngle(15)
	renderer := fitchart.NewLinearValueRenderer(area, value)

	path := renderer.BuildPath(0.3, 40)
	if path != nil {
		t.Errorf("Expected path to be nil when startAngle > animationSeek")
	}
}

func TestLinearValueRendererPublic_CalculateSweepAngle_BranchesWithDifferentData(t *testing.T) {
	area := fitchart.RectF{5, 5, 90, 90}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(5)
	value.SetSweepAngle(25)
	renderer := fitchart.NewLinearValueRenderer(area, value)

	_ = renderer.BuildPath(0.3, 20) // force totalSizeOfValue > animationSeek
	_ = renderer.BuildPath(0.6, 40) // force totalSizeOfValue <= animationSeek
	// Test passes if these do not panic.
}