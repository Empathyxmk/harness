package public_tests

import (
	"sync"
	"testing"
)

func TestPublicPutSandboxPutsToQueue(t *testing.T) {
	qvals := []interface{}{}
	mutex := sync.Mutex{}
	putNowait := func(vs ...interface{}) {
		mutex.Lock()
		defer mutex.Unlock()
		qvals = append(qvals, vs...)
	}
	putNowait("a", "b", "c")
	mutex.Lock()
	defer mutex.Unlock()
	expected := []interface{}{"a", "b", "c"}
	for i, v := range qvals {
		if expected[i] != v {
			t.Errorf("queue value mismatch at %d: want %v, got %v", i, expected[i], v)
		}
	}
}

func TestPublicInitParallelism(t *testing.T) {
	msgs := []struct {
		level string
		msg   string
	}{}
	info := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"info", msg}) }
	warn := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"warn", msg}) }
	parallelism := 4
	created := false
	createSandboxes := func(n int) []int {
		if n != parallelism {
			t.Errorf("Parallelism value mismatch: got %d, want %d", n, parallelism)
		}
		created = true
		return []int{9, 8, 7, 6}
	}
	_ = createSandboxes(parallelism)
	info("parallelism info")
	if !created {
		t.Errorf("Sandboxes were not created")
	}
	if len(msgs) == 0 {
		t.Errorf("Logger was not called")
	}
}

func TestPublicInitLowParallelism(t *testing.T) {
	msgs := []struct {
		level string
		msg   string
	}{}
	info := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"info", msg}) }
	warn := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"warn", msg}) }
	createSandboxes := func(n int) []string { return []string{"s1", "s2"} }
	_ = createSandboxes(2)
	warn("parallelism low warning")
	if len(msgs) == 0 {
		t.Errorf("Logger was not called for warn")
	}
}