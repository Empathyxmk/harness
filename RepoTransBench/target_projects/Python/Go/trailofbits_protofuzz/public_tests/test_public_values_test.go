package public_tests

import (
	"testing"
	"math"
)

func integralValueGenPublic() []int {
	vals := []int{-3, -2, -1, 0, 1, 2, 3, 4}
	return vals
}

func float32ValueGenPublic() []float32 {
	vals := []float32{-3.7, -1.0, 0, 0.25, 1.1, 2.2, 99.99, 1e10}
	return vals
}

func stringValueGenPublic() []string {
	vals := []string{"hello", "", "foo", "bar!", "baz", "asdf", "qwerty", "💡", "000", "#"}
	return vals
}

func TestIntegralValueGenPublic(t *testing.T) {
	vals := integralValueGenPublic()
	valseen := make(map[int]bool)
	for _, v := range vals {
		if _, ok := interface{}(v).(int); !ok {
			t.Errorf("Value %v is not int", v)
		}
		valseen[v] = true
	}
	if len(valseen) != len(vals) {
		t.Errorf("Non-unique ints found")
	}
	hasNeg, hasPos := false, false
	for _, v := range vals {
		if v < 0 {
			hasNeg = true
		}
		if v >= 0 {
			hasPos = true
		}
	}
	if !hasNeg || !hasPos {
		t.Errorf("Did not see both negative and non-negative integers")
	}
	if len(vals) <= 5 {
		t.Errorf("Expected more than 5 values, got %d", len(vals))
	}
}

func TestFloat32ValueGenPublic(t *testing.T) {
	vals := float32ValueGenPublic()
	uniq := make(map[float32]bool)
	for _, v := range vals {
		if _, ok := interface{}(v).(float32); !ok {
			t.Errorf("Value %v is not float32", v)
		}
		uniq[v] = true
	}
	if len(uniq) != len(vals) {
		t.Errorf("Non-unique floats found")
	}
	near := false
	away := false
	for _, v := range vals {
		if math.Abs(float64(v)) < 1.0 {
			near = true
		}
		if math.Abs(float64(v)) > 1.0 {
			away = true
		}
	}
	if !near || !away {
		t.Errorf("Did not get some floats below and above 1.0")
	}
	if len(vals) <= 7 {
		t.Errorf("Expected more than 7 values, got %d", len(vals))
	}
}

func TestStringValueGenPublic(t *testing.T) {
	vals := stringValueGenPublic()
	uniq := make(map[string]bool)
	hasLong := false
	for _, v := range vals {
		if _, ok := interface{}(v).(string); !ok {
			t.Errorf("Value %v is not string", v)
		}
		uniq[v] = true
		if len([]rune(v)) > 3 {
			hasLong = true
		}
	}
	if len(uniq) != len(vals) {
		t.Errorf("Non-unique strings found")
	}
	if !hasLong {
		t.Errorf("Did not find some longer string")
	}
	if len(vals) <= 5 {
		t.Errorf("Expected more than 5 values, got %d", len(vals))
	}
}