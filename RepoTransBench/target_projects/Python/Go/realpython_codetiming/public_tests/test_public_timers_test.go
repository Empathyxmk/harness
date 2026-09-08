package public_tests

import (
	"math"
	"testing"
)

type Timers struct {
	_data map[string][]float64
}

func NewTimers() *Timers {
	return &Timers{_data: make(map[string][]float64)}
}
func (t *Timers) add(key string, val float64) {
	t._data[key] = append(t._data[key], val)
}
func (t *Timers) count(key string) int { return len(t._data[key]) }
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
func (t *Timers) clear()              { t._data = make(map[string][]float64) }

func TestAddAndTotalAndCountPublic(t *testing.T) {
	timers := NewTimers()
	timers.add("alpha", 0.5)
	timers.add("alpha", 0.7)
	if timers.count("alpha") != 2 {
		t.Errorf("Expected 2 got %d", timers.count("alpha"))
	}
	if timers.total("alpha") != 1.2 {
		t.Errorf("Expected total 1.2 got %f", timers.total("alpha"))
	}
}

func TestMinMaxMeanMedianStdevPublic(t *testing.T) {
	timers := NewTimers()
	vals := []float64{4.0, 5.5, 6.5}
	for _, v := range vals {
		timers.add("y", v)
	}
	if timers.min("y") != 4.0 {
		t.Errorf("min want 4.0 got %f", timers.min("y"))
	}
	if timers.max("y") != 6.5 {
		t.Errorf("max want 6.5 got %f", timers.max("y"))
	}
	if timers.mean("y") != (4.0+5.5+6.5)/3 {
		t.Errorf("mean wrong")
	}
	if timers.median("y") != 5.5 {
		t.Errorf("median want 5.5 got %f", timers.median("y"))
	}
	s := timers.stdev("y")
	if math.IsNaN(s) || s <= 0 {
		t.Errorf("stdev should be > 0, got %v", s)
	}
}

func TestStdevNanForOneEntryPublic(t *testing.T) {
	timers := NewTimers()
	timers.add("single_public", 13.6)
	if !math.IsNaN(timers.stdev("single_public")) {
		t.Errorf("stdev should be NaN when len==1, got %v", timers.stdev("single_public"))
	}
}

func TestMinMaxZeroIfEmptyPublic(t *testing.T) {
	timers := NewTimers()
	timers._data["emptycase"] = []float64{}
	if timers.min("emptycase") != 0 {
		t.Errorf("min should be 0 for empty, got %f", timers.min("emptycase"))
	}
	if timers.max("emptycase") != 0 {
		t.Errorf("max should be 0 for empty, got %f", timers.max("emptycase"))
	}
}
func TestMeanMedianZeroIfEmptyPublic(t *testing.T) {
	timers := NewTimers()
	timers._data["emptycase"] = []float64{}
	if timers.mean("emptycase") != 0 {
		t.Errorf("mean should be 0 got %f", timers.mean("emptycase"))
	}
	if timers.median("emptycase") != 0 {
		t.Errorf("median should be 0 got %f", timers.median("emptycase"))
	}
}

func TestClearPublic(t *testing.T) {
	timers := NewTimers()
	timers.add("bar", 2.4)
	timers.clear()
	if len(timers._data) != 0 {
		t.Errorf("Expected empty timings after clear")
	}
}

func TestPanicTotalNoTimingsPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("should panic for missing key")
		}
	}()
	timers := NewTimers()
	timers.total("ghost")
}

func TestPanicStdevKeyErrorIfMissingPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("should panic for missing key on stdev")
		}
	}()
	timers := NewTimers()
	timers.stdev("MISSING")
}