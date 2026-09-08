package public_tests

import (
	"fitchart"
	"testing"
)

func TestRendererFactoryPublic_CreateRenderer_ReturnsLinearValueRendererWithDifferentArea(t *testing.T) {
	value := fitchart.NewFitChartValue(1, 2)
	area := fitchart.RectF{1, 2, 80, 60}
	renderer := fitchart.RendererFactory{}.Create(area, value, fitchart.LINEAR)
	if _, ok := renderer.(*fitchart.LinearValueRenderer); !ok {
		t.Errorf("Expected LinearValueRenderer, got %T", renderer)
	}
}

func TestRendererFactoryPublic_CreateRenderer_ReturnsOverdrawValueRendererWithDifferentArea(t *testing.T) {
	value := fitchart.NewFitChartValue(1, 2)
	area := fitchart.RectF{3, 4, 70, 30}
	renderer := fitchart.RendererFactory{}.Create(area, value, fitchart.OVERDRAW)
	if _, ok := renderer.(*fitchart.OverdrawValueRenderer); !ok {
		t.Errorf("Expected OverdrawValueRenderer, got %T", renderer)
	}
}