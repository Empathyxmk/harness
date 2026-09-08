package public_tests

import (
	"testing"
	"github.com/packt-oop3/goport/internal/chapter12"
)

func TestMeanNewData(t *testing.T) {
	data := chapter12.NewStatsList([]float64{10, 20, 30, 40})
	if data.Mean() != 25 {
		t.Errorf("Expected mean 25, got %f", data.Mean())
	}
}

func TestLenIsLen(t *testing.T) {
	data := chapter12.NewStatsList([]float64{11, 15, 21})
	if data.Len() != 3 {
		t.Errorf("Expected length 3, got %d", data.Len())
	}
}

func TestSumPublic(t *testing.T) {
	data := chapter12.NewStatsList([]float64{4, 5, 7})
	sum := 0.0
	for i := 0; i < data.Len(); i++ {
		sum += data.Get(i)
	}
	if sum != 16 {
		t.Errorf("Expected sum 16, got %v", sum)
	}
}