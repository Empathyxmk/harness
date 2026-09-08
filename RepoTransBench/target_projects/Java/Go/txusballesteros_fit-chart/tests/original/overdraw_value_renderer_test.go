package original

import (
	"fitchart"
	"testing"
)

func TestOverdrawValueRenderer_BuildPath(t *testing.T) {
	area := fitchart.RectF{0, 0, 100, 100}
	value := fitchart.NewFitChartValue(0, 0)
	value.SetStartAngle(10)
	value.SetSweepAngle(100)
	renderer := fitchart.NewOverdrawValueRenderer(area, value)

	path := renderer.BuildPath(0.5, 50)
	if path == nil {
		t.Error("Expected path to be non-nil")
	}
}