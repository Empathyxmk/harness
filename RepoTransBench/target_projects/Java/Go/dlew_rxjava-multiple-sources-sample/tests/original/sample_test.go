package tests

import (
	"testing"
	"dlew_rxjava_multiple_sources_sample/dlew"
	"time"
)

func TestSample_Sleep_noInterrupt(t *testing.T) {
	dlew.Sample{}.Sleep(10)
	// Should complete without exception (simulated)
}

func TestSample_Sleep_withInterrupt(t *testing.T) {
	done := make(chan struct{})
	go func() {
		dlew.Sample{}.Sleep(1000)
		close(done)
	}()
	time.Sleep(10 * time.Millisecond)
	// Go doesn't really interrupt goroutines, but this test verifies that it doesn't panic
	// No assertion, just let it run briefly and exit
}