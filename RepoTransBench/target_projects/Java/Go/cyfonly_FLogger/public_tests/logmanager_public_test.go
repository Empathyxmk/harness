package public_tests

import (
	"testing"
)

type DummyLogManager struct{}

var dummyLogManager = &DummyLogManager{}

func GetDummyLogManager() *DummyLogManager {
	return dummyLogManager
}

func (l *DummyLogManager) Close() {}

func TestSingletonAndClosePublic(t *testing.T) {
	lm1 := GetDummyLogManager()
	lm2 := GetDummyLogManager()
	if lm1 != lm2 {
		t.Errorf("Expected singleton log manager instances")
	}
	// Just call close to make sure no exception occurs
	lm1.Close()
	// No assertion needed, just ensuring no panic or error
}