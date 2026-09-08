package original

import (
	"math"
	"testing"
	"time"
)

func CputimeDecorator(fn func() int) func() int {
	return func() int {
		start := time.Now()
		for i := 0; i < 1000; i++ {
			_ = math.Pow(float64(i), float64(i))
		}
		_ = time.Since(start).Seconds()
		return fn()
	}
}

func TestCputimeDecoratorBasic(t *testing.T) {
	test := CputimeDecorator(func() int { return 1 })
	r := test()
	if r != 1 {
		t.Errorf("Expected return value 1, got: %v", r)
	}
}