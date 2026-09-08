package public_tests

import (
	"testing"
)

type Constants struct {
	Title        string
	WatcherSuffix string
}

func TestConstantsHaveTitleAndSuffix(t *testing.T) {
	constants := &Constants{Title: "SomeTitle", WatcherSuffix: "_watcher"}
	if constants.Title == "" {
		t.Error("TITLE not in constants")
	}
	if constants.WatcherSuffix == "" {
		t.Error("WATCHER_SUFFIX not in constants")
	}
}