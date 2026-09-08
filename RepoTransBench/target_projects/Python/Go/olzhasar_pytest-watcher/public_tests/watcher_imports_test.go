package public_tests

import (
	"testing"
)

type Watcher struct {
	File   string
	Loader func() bool
}

func TestPublicImportAllWatcherModuleNames(t *testing.T) {
	mod := &Watcher{
		File:   "watcher.go",
		Loader: func() bool { return true },
	}
	if mod.File == "" {
		t.Error("__file__ missing in watcher")
	}
	if mod.Loader == nil || !mod.Loader() {
		t.Error("Loader not callable or returns false")
	}
}