package original

import (
	"math"
	"testing"
)

type Timers struct {
	_data    map[string][]float64
}

func NewTimers() *Timers {
	return &Timers{_data: make(map[string][]float64)}
}
func (t *Timers) add(key string, val float64) {
	t._data[key] = append(t._data[key], val)
}
func (t *Timers) count(key string) int {
	return len(t._data[key])
}
func (t *Timers) total(key string) float64 {
	vals := t._data[key]
	if vals == nil {
		panic("KeyError")
	}
	tot := 0.0
	for _, v := range vals {
		tot += v
	}
	return tot
}
func (t *Timers) min(key string) float64 {
	vals := t._data[key]
	if len(vals) == 0 {
		return 0
	}
	min := vals[0]
	for _, v := range vals {
		if v < min {
			min = v
		}
	}
	return min
}
func (t *Timers) max(key string) float64 {
	vals := t._data[key]
	if len(vals) == 0 {
		return 0
	}
	max := vals[0]
	for _, v := range vals {
		if v > max {
			max = v
		}
	}
	return max
}
func (t *Timers) mean(key string) float64 {
	vals := t._data[key]
	if len(vals) == 0 {
		return 0
	}
	sum := 0.0
	for _, v := range vals {
		sum += v
	}
	return sum / float64(len(vals))
}
func (t *Timers) median(key string) float64 {
	vals := t._data[key]
	l := len(vals)
	if l == 0 {
		return 0
	}
	sorted := make([]float64, l)
	copy(sorted, vals)
	for i := 1; i < l; i++ {
		for j := 0; j < i; j++ {
			if sorted[j] > sorted[i] {
				sorted[j], sorted[i] = sorted[i], sorted[j]
			}
		}
	}
	if l%2 == 1 {
		return sorted[l/2]
	}
	return (sorted[l/2-1] + sorted[l/2]) / 2
}
func (t *Timers) stdev(key string) float64 {
	vals := t._data[key]
	if len(vals) == 1 {
		return math.NaN()
	}
	if len(vals) == 0 {
		panic("KeyError")
	}
	m := t.mean(key)
	var sumsq float64
	for _, v := range vals {
		d := v - m
		sumsq += d * d
	}
	return math.Sqrt(sumsq / float64(len(vals)))
}

func (t *Timers) clear() {
	t._data = make(map[string][]float64)
}

func TestAddAndTotalAndCount(t *testing.T) {
	timers := NewTimers()
	timers.add("t1", 1.0)
	timers.add("t1", 2.0)
	if timers.count("t1") != 2 {
		t.Errorf("count(t1): want 2, got %v", timers.count("t1"))
	}
	if timers.total("t1") != 3.0 {
		t.Errorf("total(t1): want 3.0, got %v", timers.total("t1"))
	}
}

func TestMinMaxMeanMedianStdev(t *testing.T) {
	timers := NewTimers()
	vals := []float64{1.0, 2.0, 3.0}
	for _, v := range vals {
		timers.add("x", v)
	}
	if timers.min("x") != 1.0 {
		t.Errorf("min(x): want 1.0, got %v", timers.min("x"))
	}
	if timers.max("x") != 3.0 {
		t.Errorf("max(x): want 3.0, got %v", timers.max("x"))
	}
	if timers.mean("x") != 2.0 {
		t.Errorf("mean(x): want 2.0, got %v", timers.mean("x"))
	}
	if timers.median("x") != 2.0 {
		t.Errorf("median(x): want 2.0, got %v", timers.median("x"))
	}
	s := timers.stdev("x")
	if math.IsNaN(s) || s <= 0 {
		t.Errorf("stdev(x): want positive float, got %v", s)
	}
}

func TestStdevNanForOneEntry(t *testing.T) {
	timers := NewTimers()
	timers.add("single", 2.345)
	if !math.IsNaN(timers.stdev("single")) {
		t.Errorf("stdev: want NaN for single entry, got %v", timers.stdev("single"))
	}
}

func TestMinMaxZeroIfEmpty(t *testing.T) {
	timers := NewTimers()
	timers._data["e"] = []float64{}
	if timers.min("e") != 0 {
		t.Errorf("min(e): want 0, got %v", timers.min("e"))
	}
	if timers.max("e") != 0 {
		t.Errorf("max(e): want 0, got %v", timers.max("e"))
	}
}
func TestMeanMedianZeroIfEmpty(t *testing.T) {
	timers := NewTimers()
	timers._data["e"] = []float64{}
	if timers.mean("e") != 0 {
		t.Errorf("mean(e): want 0, got %v", timers.mean("e"))
	}
	if timers.median("e") != 0 {
		t.Errorf("median(e): want 0, got %v", timers.median("e"))
	}
}

func TestClear(t *testing.T) {
	timers := NewTimers()
	timers.add("foo", 1.2)
	timers.clear()
	if len(timers._data) != 0 {
		t.Errorf("Expected no timings after clear, got %d", len(timers._data))
	}
}

func TestPanicOnMissingKeyForTotal(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic on missing key for total")
		}
	}()
	timers := NewTimers()
	timers.total("missing")
}

func TestPanicOnMissingKeyForStdev(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic on missing key for stdev")
		}
	}()
	timers := NewTimers()
	timers.stdev("N/A")
}

// Simulate setitem/key error/TypeError as panic for simplicity