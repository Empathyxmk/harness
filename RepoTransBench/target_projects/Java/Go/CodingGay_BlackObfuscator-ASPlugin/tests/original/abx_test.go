package original

import (
	"testing"
	"time"
)

// Fake implementation of Abx.go() just for test, should always return true
func abxGo() bool {
	return time.Now().UnixMilli() > 0
}

func TestGoAlwaysTrue(t *testing.T) {
	if !abxGo() {
		t.Error("abxGo should always return true, but got false")
	}
}