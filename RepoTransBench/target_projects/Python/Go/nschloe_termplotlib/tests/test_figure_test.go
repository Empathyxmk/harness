package tests

import (
	"testing"
	"reflect"
)

// Simulate Figure type
type Figure struct{}

func NewFigure() *Figure {
	return &Figure{}
}

func TestFigureInit(t *testing.T) {
	fig := NewFigure()
	if reflect.TypeOf(fig) != reflect.TypeOf(&Figure{}) {
		t.Errorf("fig is not of type *Figure")
	}
}