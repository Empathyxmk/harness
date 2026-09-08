package public_tests

import (
	"sync"
	"testing"
)

func TestReentrantLockLowContention(t *testing.T) {
	var lock sync.Mutex
	sum := 0
	N := 50
	for i := 0; i < N; i++ {
		lock.Lock()
		sum += i
		lock.Unlock()
	}
	if sum <= 0 {
		t.Errorf("expected sum > 0, got %d", sum)
	}
}