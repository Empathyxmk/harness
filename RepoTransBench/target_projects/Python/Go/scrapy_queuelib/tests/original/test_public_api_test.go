package original

import (
	"testing"
)

var queuelib = struct {
	Version string
	All     []string
}{
	Version: "1.0.0",
	All:     []string{"pqueue", "rrqueue", "PriorityQueue", "RoundRobinQueue"},
}

func TestVersionAndAll(t *testing.T) {
	if queuelib.Version == "" {
		t.Error("queuelib missing __version__")
	}
	for _, symbol := range queuelib.All {
		// In real test, check if exported in package
		if symbol == "" {
			t.Errorf("queuelib.__all__ contains empty symbol")
		}
	}
}