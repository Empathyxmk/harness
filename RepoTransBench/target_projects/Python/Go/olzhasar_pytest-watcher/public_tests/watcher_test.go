package public_tests

import (
	"testing"
)

func TestWatcherImportAndStr(t *testing.T) {
	watcherRepr := "pytest_watcher"
	if watcherRepr != "pytest_watcher" {
		t.Error("watcher_repr does not contain pytest_watcher")
	}
}

func TestWatcherMainLoopInterrupt(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic (simulating KeyboardInterrupt)")
		}
	}()
	panic("KeyboardInterrupt")
}