package public_tests

import (
	"fitchart"
	"testing"
)

type testRenderer struct {
	*fitchart.BaseRenderer
}

func newTestRenderer(area fitchart.RectF, value *fitchart.FitChartValue) *testRenderer {
	return &testRenderer{fitchart.NewBaseRenderer(area, value)}
}

func TestBaseRendererPublic_GetDrawingAreaAndValue_WithDifferentAreaAndValue(t *testing.T) {
	area := fitchart.RectF{Left: 10, Top: 12, Right: 34, Bottom: 56}
	value := fitchart.NewFitChartValue(55, 0xABCDEF)
	renderer := newTestRenderer(area, value)
	if renderer.GetDrawingArea() != area {
		t.Errorf("Expected area %+v, got %+v", area, renderer.GetDrawingArea())
	}
	if renderer.GetValue() != value {
		t.Errorf("Expected value %+v, got %+v", value, renderer.GetValue())
	}
}