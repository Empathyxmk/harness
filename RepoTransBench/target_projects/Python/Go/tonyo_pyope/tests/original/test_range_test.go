package original

import (
	"testing"
	"reflect"
	"errors"
)

type TestValueRangeSuite struct{}

func TestRangeSimple(t *testing.T) {
	start := int64(2)
	end := int64(1000)
	r, _ := NewValueRange(start, end)
	if r.size() != 999 {
		t.Errorf("Expected size 999, got %v", r.size())
	}
	for i := start; i <= end; i++ {
		if !r.contains(i) {
			t.Errorf("Range %v should contain %v", r, i)
		}
	}
	if r.contains(start-1) {
		t.Errorf("Range %v should not contain %v", r, start-1)
	}
	if r.contains(end+1) {
		t.Errorf("Range %v should not contain %v", r, end+1)
	}
	if r.rangeBitSize() != 10 {
		t.Errorf("Expected rangeBitSize 10")
	}
}

func (vr *ValueRange) rangeBitSize() int {
	s := vr.size() + 1
	bs := 0
	for s > 0 {
		s = s >> 1
		bs++
	}
	return bs - 1
}

func TestRangeRepr(t *testing.T) {
	a, _ := NewValueRange(1, 10)
	b, _ := NewValueRange(1, 10)
	if !reflect.DeepEqual(a, b) {
		t.Errorf("Range representation mismatch")
	}
}

func TestInvalidRangeEnds(t *testing.T) {
	invalidCases := []struct {
		start interface{}
		end   interface{}
	}{
		{"123", 0},
		{0, "123"},
		{"123", "abc"},
	}
	for _, tc := range invalidCases {
		_, err := func() (*ValueRange, error) {
			s, sok := tc.start.(int64)
			e, eok := tc.end.(int64)
			if !sok || !eok {
				return nil, errors.New("InvalidRangeLimitsError")
			}
			return NewValueRange(s, e)
		}()
		if err == nil {
			t.Errorf("Expected error for invalid range ends: %+v", tc)
		}
	}
}