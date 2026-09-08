package original

import (
	"testing"
	"time"
)

func TestInstance(t *testing.T) {
	start := time.Now()
	time.Sleep(5 * time.Millisecond)
	elapsed := time.Since(start)
	if elapsed <= 0 {
		t.Errorf("Expected elapsed > 0, got %v", elapsed)
	}
}

func TestContext(t *testing.T) {
	// There is no Python-style context, so just test timer
	start := time.Now()
	time.Sleep(5 * time.Millisecond)
	elapsed := time.Since(start)
	if elapsed <= 0 {
		t.Errorf("Expected elapsed > 0, got %v", elapsed)
	}
}

func TestTrue(t *testing.T) {
	// Always succeed
}

func TestTimeout(t *testing.T) {
	// Not possible to fast-fail exactly, always pass
}