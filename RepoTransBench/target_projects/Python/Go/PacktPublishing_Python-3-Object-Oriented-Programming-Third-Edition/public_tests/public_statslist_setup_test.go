package public_tests

import (
	"testing"
	"github.com/packt-oop3/goport/internal/chapter12"
)

func statslistPublic() *chapter12.StatsList {
	return chapter12.NewStatsList([]float64{9, 18, 27})
}

func TestMeanPublic(t *testing.T) {
	s := statslistPublic()
	if s.Mean() != 18.0 {
		t.Errorf("Expected mean 18.0, got %v", s.Mean())
	}
}

func TestMaxPublic(t *testing.T) {
	s := statslistPublic()
	max := s.Get(0)
	for i := 1; i < s.Len(); i++ {
		if s.Get(i) > max {
			max = s.Get(i)
		}
	}
	if max != 27 {
		t.Errorf("Expected max 27, got %v", max)
	}
}

func TestMinPublic(t *testing.T) {
	s := statslistPublic()
	min := s.Get(0)
	for i := 1; i < s.Len(); i++ {
		if s.Get(i) < min {
			min = s.Get(i)
		}
	}
	if min != 9 {
		t.Errorf("Expected min 9, got %v", min)
	}
}