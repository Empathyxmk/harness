package public_tests

import (
	"os"
	"testing"
)

func TestPublicDaemonPlaceholder1(t *testing.T) {
	if 42*2 != 84 {
		t.Error("42 * 2 != 84")
	}
}

func TestPublicDaemonPlaceholder2(t *testing.T) {
	if os.PathSeparator != '/' && os.PathSeparator != '\\' {
		t.Error("PathSeparator is not '/' or '\\'")
	}
}

func TestPublicDaemonPlaceholder3(t *testing.T) {
	a := []int{1*1, 3*3, 5*5}
	sum := 0
	for _, v := range a {
		sum += v
	}
	if sum != 35 {
		t.Errorf("expected sum to be 35, got %d", sum)
	}
}