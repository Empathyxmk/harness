package original

import (
	"testing"
)

func TestDirectiveCall_Basic(t *testing.T) {
	// simulate #macro inc(int x)${x+1}#end#call inc(1)
	result := inc(1)
	if result != 2 {
		t.Errorf("Expected 2, got %d", result)
	}
}
func inc(x int) int {
	return x + 1
}