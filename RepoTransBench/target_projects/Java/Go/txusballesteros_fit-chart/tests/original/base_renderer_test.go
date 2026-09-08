package original

import (
	"fitchart"
	"testing"
)

type concreteRenderer struct {
	*fitchart.BaseRenderer
}
func newConcreteRenderer(area fitchart.RectF, value *fitchart.FitChartValue) *concreteRenderer {
	return &concreteRenderer{fitchart.NewBaseRenderer(area, value)}
}

func TestBaseRenderer_Getters(t *testing.T) {
	area := fitchart.RectF{Left: 1, Top: 2, Right: 3, Bottom: 4}
	val := fitchart.NewFitChartValue(42, 0xDEADBEEF)
	cr := newConcreteRenderer(area, val)

	gotArea := cr.GetDrawingArea()
	gotVal := cr.GetValue()

	if gotArea != area {
		t.Errorf("expected area %+v, got %+v", area, gotArea)
	}
	if gotVal != val {
		t.Errorf("expected value %+v, got %+v", val, gotVal)
	}
}