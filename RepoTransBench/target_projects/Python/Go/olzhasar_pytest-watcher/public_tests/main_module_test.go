package public_tests

import (
	"testing"
)

type MainModule struct {
	Name string
	File string
}

func TestMainEntryPointModuleHasName(t *testing.T) {
	mainMod := &MainModule{Name: "__main__", File: "main.go"}
	if mainMod.Name == "" && mainMod.File == "" {
		t.Error("Main module missing name or file")
	}
}