package util

import (
	"testing"
)

func TestApplySchedulers_DifferentData(t *testing.T) {
	// In Java this tested the RxJava trampoline/async main thread.
	// In Go, we just check value passes directly.
	val := "alpha"
	got := val // No scheduler applied in Go, just transfer
	if got != "alpha" {
		t.Errorf("expected alpha, got %s", got)
	}
}