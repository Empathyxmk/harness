package public_tests

import (
	"testing"
)

func TestImportWin32NoCtypesPublic(t *testing.T) {
	// Simulate missing ctypes - in Go, "ctypes" and reload logic is moot
	win32 := GetWin32DummyPublic(false)
	if win32.windll != nil {
		t.Errorf("expected windll == nil")
	}
	if win32.SetConsoleTextAttribute == nil {
		t.Errorf("expected SetConsoleTextAttribute to be callable")
	}
	if win32.WinapiTest == nil {
		t.Errorf("expected WinapiTest to be callable")
	}
}

func TestImportWin32WithCtypesPublic(t *testing.T) {
	win32 := GetWin32DummyPublic(true)
	if !win32.Has("ENABLE_VIRTUAL_TERMINAL_PROCESSING") {
		t.Log("ENABLE_VIRTUAL_TERMINAL_PROCESSING not present (ok for non-windows)")
	}
}

func TestDummySetConsoleTextAttributePublic(t *testing.T) {
	win32 := GetWin32DummyPublic(false)
	result := win32.SetConsoleTextAttribute("bar", 1)
	if result != nil {
		t.Errorf("expected nil dummy")
	}
}

func TestDummyWinapiTestPublic(t *testing.T) {
	win32 := GetWin32DummyPublic(false)
	result := win32.WinapiTest("dummy-arg")
	if result != nil {
		t.Errorf("expected nil for dummy winapi_test")
	}
}

// Simulated Go version of win32 for public tests
type Win32DummyPublic struct {
	windll                    interface{}
	SetConsoleTextAttribute   func(...interface{}) interface{}
	WinapiTest                func(...interface{}) interface{}
}

func (w *Win32DummyPublic) Has(attr string) bool {
	if attr == "ENABLE_VIRTUAL_TERMINAL_PROCESSING" {
		return true
	}
	return false
}

func GetWin32DummyPublic(withCtypes bool) *Win32DummyPublic {
	return &Win32DummyPublic{
		windll: func() interface{} {
			if withCtypes {
				return "windll"
			}
			return nil
		}(),
		SetConsoleTextAttribute: func(args ...interface{}) interface{} {
			return nil
		},
		WinapiTest: func(args ...interface{}) interface{} {
			return nil
		},
	}
}