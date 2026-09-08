package public_tests

import (
	"fitchart"
	"testing"
)

func TestOverdrawValueRendererPublic_BuildPath_WithOtherAngles(t *testing.T) {
	area := fitchart.RectF{2, 2, 50, 50}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(30)
	value.SetSweepAngle(45)
	renderer := fitchart.NewOverdrawValueRenderer(area, value)

	path := renderer.BuildPath(0.6, 35)
	if path == nil {
		t.Error("Expected path to be non-nil")
	}
}