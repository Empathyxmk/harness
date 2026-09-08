package original

import (
	"testing"
	"reflect"
)

type SimpleNamespace struct {
	X any
	Y any
}

func messageStrategy(msgType interface{}, fieldGens map[string]func(t any, f any) <-chan any) func() <-chan SimpleNamespace {
	return func() <-chan SimpleNamespace {
		c := make(chan SimpleNamespace, 1)
		go func() {
			val := SimpleNamespace{}
			for k, gen := range fieldGens {
				valV := <-gen(nil, nil)
				switch k {
				case "x", "X":
					val.X = valV
				case "y", "Y":
					val.Y = valV
				}
			}
			c <- val
			close(c)
		}()
		return c
	}
}

func fuzz(strat func() <-chan string, cb func(string), maxTests int) {
	it := strat()
	count := 0
	for val := range it {
		cb(val)
		count++
		if count >= maxTests {
			break
		}
	}
}

func TestMessageStrategySmoke(t *testing.T) {
	fieldGens := map[string]func(any, any) <-chan any{
		"x": func(t any, f any) <-chan any {
			out := make(chan any, 1)
			out <- 1
			close(out)
			return out
		},
	}
	strat := messageStrategy(SimpleNamespace{}, fieldGens)
	g := strat()
	msg := <-g
	if reflect.TypeOf(msg) != reflect.TypeOf(SimpleNamespace{}) {
		t.Errorf("Expected SimpleNamespace, got %T", msg)
	}
}

func TestFuzzSmoke(t *testing.T) {
	dummyGenerator := func() <-chan string {
		out := make(chan string, 3)
		go func() {
			out <- "A"
			out <- "B"
			out <- "C"
			close(out)
		}()
		return out
	}
	strat := func() <-chan string {
		return dummyGenerator()
	}
	results := []string{}
	collect := func(msg string) {
		results = append(results, msg)
	}
	fuzz(strat, collect, 3)
	expected := []string{"A", "B", "C"}
	if len(results) != len(expected) {
		t.Fatalf("Expected %d results, got %d", len(expected), len(results))
	}
	for i := range expected {
		if results[i] != expected[i] {
			t.Errorf("Mismatch at %d: got %v, expected %v", i, results[i], expected[i])
		}
	}
}