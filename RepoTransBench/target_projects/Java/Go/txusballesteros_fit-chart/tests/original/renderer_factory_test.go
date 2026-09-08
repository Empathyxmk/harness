package original

import (
	"fitchart"
	"testing"
)

func TestRendererFactory_ReturnsLinearRenderer(t *testing.T) {
	value := fitchart.NewFitChartValue(3, 10)
	rect := fitchart.RectF{0, 0, 100, 100}
	renderer := fitchart.RendererFactory{}.GetRenderer(fitchart.LINEAR, value, rect)
	if _, ok := renderer.(*fitchart.LinearValueRenderer); !ok {
		t.Errorf("Expected LinearValueRenderer type, got %T", renderer)
	}
}

func TestRendererFactory_ReturnsOverdrawRenderer(t *testing.T) {
	value := fitchart.NewFitChartValue(3, 10)
	rect := fitchart.RectF{0, 0, 100, 100}
	renderer := fitchart.RendererFactory{}.GetRenderer(fitchart.OVERDRAW, value, rect)
	if _, ok := renderer.(*fitchart.OverdrawValueRenderer); !ok {
		t.Errorf("Expected OverdrawValueRenderer type, got %T", renderer)
	}
}