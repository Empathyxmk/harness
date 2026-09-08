package public_tests

import (
	"testing"
	"reflect"
)

// Simulate Figure and Axes types
type Axes struct {
	id int
}

type Figure struct {
	counter int
}

func NewFigure() *Figure {
	return &Figure{}
}

// Simulate Figure.AddSubplot
func (f *Figure) AddSubplot(id int) *Axes {
	return &Axes{id: id}
}

func TestFigureCreationAndAxes(t *testing.T) {
	f := NewFigure()
	ax := f.AddSubplot(111)
	// "from termplotlib.figure import Axes" is equivalent to Axes type here
	if reflect.TypeOf(ax) != reflect.TypeOf(&Axes{}) {
		t.Errorf("ax is not of type *Axes")
	}
	ax2 := f.AddSubplot(112)
	if reflect.TypeOf(ax2) != reflect.TypeOf(&Axes{}) {
		t.Errorf("ax2 is not of type *Axes")
	}
	if ax == ax2 {
		t.Errorf("ax and ax2 are the same, expected different Axes")
	}
}