package original

import (
	"testing"
	"math"
	"math/rand"
	"time"
)

func integralValueGen() <-chan int {
	out := make(chan int, 8)
	go func() {
		for i := 0; i < 8; i++ {
			out <- i - 4
		}
		close(out)
	}()
	return out
}

func float32ValueGen() <-chan float32 {
	out := make(chan float32, 8)
	go func() {
		for i := 0; i < 8; i++ {
			out <- float32(math.Sin(float64(i)))
		}
		close(out)
	}()
	return out
}

func stringValueGen() <-chan string {
	out := make(chan string, 6)
	vals := []string{"alpha", "beta", "gamma", "delta", "", "Z"}
	go func() {
		for _, v := range vals {
			out <- v
		}
		close(out)
	}()
	return out
}

func TestIntegralValueGen(t *testing.T) {
	g := integralValueGen()
	vals := make([]int, 0, 8)
	for i := 0; i < 8; i++ {
		vals = append(vals, <-g)
	}
	for _, v := range vals {
		if _, ok := interface{}(v).(int); !ok {
			t.Errorf("Value %v is not int", v)
		}
	}
}

func TestFloat32ValueGen(t *testing.T) {
	g := float32ValueGen()
	vals := make([]float32, 0, 8)
	for i := 0; i < 8; i++ {
		vals = append(vals, <-g)
	}
	for _, v := range vals {
		if _, ok := interface{}(v).(float32); !ok {
			t.Errorf("Value %v is not float32", v)
		}
	}
}

func TestStringValueGen(t *testing.T) {
	g := stringValueGen()
	vals := make([]string, 0, 6)
	for i := 0; i < 6; i++ {
		vals = append(vals, <-g)
	}
	for _, v := range vals {
		if _, ok := interface{}(v).(string); !ok {
			t.Errorf("Value %v is not string", v)
		}
	}
}