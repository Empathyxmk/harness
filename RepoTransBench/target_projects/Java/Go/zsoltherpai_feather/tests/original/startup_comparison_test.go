package original

import (
	"fmt"
	"testing"
	"time"
)

// Simulated benchmarking only for Feather replacement for Go
type A struct{}
type B struct{}
type C struct{}
type D1 struct{}
type D2 struct{}
type E struct{}

const warmup = 200
const iterations = 2000 // Reduce count for practical Go test execution

func TestStartupTime(t *testing.T) {
	benchmarkExplanation(iterations)
	// Simulate warmup
	for i := 0; i < warmup; i++ {
		newFeatherGraph()
		// Simulate other DI frameworks if desired - here just Feather
	}
	StopWatchMillis("Feather", func() {
		for i := 0; i < iterations; i++ {
			newFeatherGraph()
		}
	})
}

func benchmarkExplanation(count int) {
	fmt.Printf("Starting up DI containers & instantiating a dependency graph %d times. [Feather only in Go version]\n", count)
}

func newFeatherGraph() *A {
	// Simulate dependency graph creation
	_ = &B{}
	_ = &C{}
	_ = &D1{}
	_ = &D2{}
	_ = &E{}
	return &A{}
}

func StopWatchMillis(name string, fn func()) {
	start := time.Now()
	fn()
	fmt.Printf("Bench: %s: %v ms\n", name, time.Since(start).Milliseconds())
}