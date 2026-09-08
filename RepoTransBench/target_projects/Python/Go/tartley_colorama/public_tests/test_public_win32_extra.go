package public_tests

import "testing"

func TestWin32DummyHasEnableVTProcessingPublic(t *testing.T) {
	win32 := GetWin32DummyPublic(true)
	if !win32.Has("ENABLE_VIRTUAL_TERMINAL_PROCESSING") {
		t.Errorf("expected win32 dummy to have ENABLE_VIRTUAL_TERMINAL_PROCESSING attr")
	}
}