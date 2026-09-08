package original

import (
	"testing"
)

type DummyTrigger struct {
	emitted bool
}

func (t *DummyTrigger) Emit() {
	t.emitted = true
}

type FileSystemEvent struct {
	EventType string
	SrcPath   string
	DestPath  string
	HasDest   bool
}

type EventHandler struct {
	trigger        *DummyTrigger
	patterns       []string
	ignorePatterns []string
}

var (
	EVENT_TYPE_CREATED  = "created"
	EVENT_TYPE_DELETED  = "deleted"
	EVENT_TYPE_MODIFIED = "modified"
	EVENT_TYPE_MOVED    = "moved"
	EVENTS_WATCHED      = map[string]bool{
		EVENT_TYPE_CREATED:  true,
		EVENT_TYPE_DELETED:  true,
		EVENT_TYPE_MODIFIED: true,
		EVENT_TYPE_MOVED:    true,
	}
)

func NewEventHandler(trigger *DummyTrigger, patterns []string, ignorePatterns []string) *EventHandler {
	if patterns == nil || len(patterns) == 0 {
		patterns = []string{"*.py"}
	}
	return &EventHandler{
		trigger:        trigger,
		patterns:       patterns,
		ignorePatterns: ignorePatterns,
	}
}

func (e *EventHandler) Patterns() []string {
	return e.patterns
}
func (e *EventHandler) IgnorePatterns() []string {
	return e.ignorePatterns
}

// matchAnyPaths simulates python's watchdog.utils.patterns.match_any_paths
func matchAnyPaths(paths []string, includedPatterns []string, excludedPatterns []string) bool {
	// This is a naive simulation that only matches file extension (".py") and .env for the tests.
	for _, path := range paths {
		excluded := false
		for _, ex := range excludedPatterns {
			if ex != "" && ex == path {
				excluded = true
			}
		}
		if excluded {
			continue
		}
		for _, inc := range includedPatterns {
			// Simulate simple suffix wildcards handling for "*.py", ".env"
			if inc == "*.py" && len(path) >= 3 && path[len(path)-3:] == ".py" {
				return true
			}
			if inc == ".env" && len(path) >= 4 && path[len(path)-4:] == ".env" {
				return true
			}
			if len(inc) > 0 && inc[0] == '*' && len(path) >= len(inc)-1 &&
				path[len(path)-len(inc)+1:] == inc[1:] {
				return true
			}
			if inc == path {
				return true
			}
		}
	}
	return false
}

func (e *EventHandler) isEventWatched(event FileSystemEvent) bool {
	if _, found := EVENTS_WATCHED[event.EventType]; !found {
		return false
	}
	paths := []string{event.SrcPath}
	if event.HasDest {
		paths = append(paths, event.DestPath)
	}
	return matchAnyPaths(paths, e.Patterns(), e.IgnorePatterns())
}

func (e *EventHandler) Dispatch(event FileSystemEvent) {
	if e.isEventWatched(event) {
		e.trigger.Emit()
	} else {
		// ignored
	}
}

// --- Tests (simulate same coverage as Python) ---

func TestEventHandler_WatchedEventsTrigger(t *testing.T) {
	types := []string{EVENT_TYPE_CREATED, EVENT_TYPE_DELETED, EVENT_TYPE_MODIFIED, EVENT_TYPE_MOVED}
	for _, evType := range types {
		trigger := &DummyTrigger{}
		handler := NewEventHandler(trigger, nil, nil)
		ev := FileSystemEvent{EventType: evType, SrcPath: "main.py"}
		handler.Dispatch(ev)
		if !trigger.emitted {
			t.Errorf("Expected event type %v to trigger", evType)
		}
	}
}

func TestEventHandler_NotWatchedEventDoesNotTrigger(t *testing.T) {
	trigger := &DummyTrigger{}
	handler := NewEventHandler(trigger, nil, nil)
	ev := FileSystemEvent{EventType: "unknown", SrcPath: "main.py"}
	handler.Dispatch(ev)
	if trigger.emitted {
		t.Errorf("Unexpected trigger on event type unknown")
	}
}

func TestEventHandler_FileMovedDestWatched(t *testing.T) {
	trigger := &DummyTrigger{}
	handler := NewEventHandler(trigger, nil, nil)
	ev := FileSystemEvent{EventType: EVENT_TYPE_MOVED, SrcPath: "main.tmp", DestPath: "main.py", HasDest: true}
	handler.Dispatch(ev)
	if !trigger.emitted {
		t.Errorf("Moved file dest watched not triggering")
	}
}

func TestEventHandler_FileMovedDestNotWatched(t *testing.T) {
	trigger := &DummyTrigger{}
	handler := NewEventHandler(trigger, nil, nil)
	ev := FileSystemEvent{EventType: EVENT_TYPE_MOVED, SrcPath: "main.tmp", DestPath: "main.temp", HasDest: true}
	handler.Dispatch(ev)
	if trigger.emitted {
		t.Errorf("Moved file dest not watched but triggered")
	}
}

func TestEventHandler_PatternsDefaultWatched(t *testing.T) {
	trigger := &DummyTrigger{}
	paths := []string{"main.py", "./main.py", "/home/project/main.py"}
	for _, path := range paths {
		handler := NewEventHandler(trigger, nil, nil)
		ev := FileSystemEvent{EventType: EVENT_TYPE_CREATED, SrcPath: path}
		handler.Dispatch(ev)
	}
	if !trigger.emitted {
		t.Error("Default watched patterns should trigger trigger")
	}
}

func TestEventHandler_PatternsDefaultNotWatched(t *testing.T) {
	trigger := &DummyTrigger{}
	paths := []string{"main.pyc", "sqlite.db", "/home/project/file.txt"}
	for _, path := range paths {
		handler := NewEventHandler(trigger, nil, nil)
		ev := FileSystemEvent{EventType: EVENT_TYPE_CREATED, SrcPath: path}
		handler.Dispatch(ev)
	}
	if trigger.emitted {
		t.Error("Default not watched patterns should not trigger trigger")
	}
}

func TestEventHandler_PatternsCustomWatched(t *testing.T) {
	cases := []struct {
		patterns []string
		path     string
	}{
		{[]string{"*.txt"}, "file.txt"},
		{[]string{"main.pyc"}, "main.pyc"},
		{[]string{"/home/path/example.txt"}, "/home/path/example.txt"},
		{[]string{"*some*.txt"}, "/home/path/something.txt"},
	}
	for _, c := range cases {
		trigger := &DummyTrigger{}
		handler := NewEventHandler(trigger, c.patterns, nil)
		ev := FileSystemEvent{EventType: EVENT_TYPE_CREATED, SrcPath: c.path}
		handler.Dispatch(ev)
		if !trigger.emitted {
			t.Errorf("Custom watched pattern %v %v should trigger", c.patterns, c.path)
		}
	}
}

func TestEventHandler_PatternsCustomNotWatched(t *testing.T) {
	cases := []struct {
		patterns []string
		path     string
	}{
		{[]string{"*.txt"}, "file.txtf"},
		{[]string{"*.pyi", "*.pdb"}, "wrong.pdf"},
		{[]string{"/home/path/example.txt"}, "/home/path/wrong.txt"},
	}
	for _, c := range cases {
		trigger := &DummyTrigger{}
		handler := NewEventHandler(trigger, c.patterns, nil)
		ev := FileSystemEvent{EventType: EVENT_TYPE_CREATED, SrcPath: c.path}
		handler.Dispatch(ev)
		if trigger.emitted {
			t.Errorf("Custom NOT watched pattern %v %v triggered", c.patterns, c.path)
		}
	}
}

func TestEventHandler_PatternsIgnoreNotWatched(t *testing.T) {
	cases := []struct {
		ignorePatterns []string
		path           string
	}{
		{[]string{"ignore/*.py"}, "ignore/myfile.py"},
		{[]string{"ignore/**"}, "ignore/main.py"},
		{[]string{"*pytest*"}, "/home/project/pytest.yaml"},
	}
	for _, c := range cases {
		trigger := &DummyTrigger{}
		handler := NewEventHandler(trigger, nil, c.ignorePatterns)
		ev := FileSystemEvent{EventType: EVENT_TYPE_CREATED, SrcPath: c.path}
		handler.Dispatch(ev)
		if trigger.emitted {
			t.Errorf("Ignore pattern %v %v should not trigger", c.ignorePatterns, c.path)
		}
	}
}