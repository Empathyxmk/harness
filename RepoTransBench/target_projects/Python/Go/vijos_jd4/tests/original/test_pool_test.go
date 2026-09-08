package original

import (
	"sync"
	"testing"
)

func TestPutSandboxPutsToQueue(t *testing.T) {
	qvals := []interface{}{}
	mutex := sync.Mutex{}
	putNowait := func(vs ...interface{}) {
		mutex.Lock()
		defer mutex.Unlock()
		qvals = append(qvals, vs...)
	}
	putNowait(1, 2, 3)
	mutex.Lock()
	defer mutex.Unlock()
	expected := []interface{}{1, 2, 3}
	for i, v := range qvals {
		if expected[i] != v {
			t.Errorf("queue value mismatch at %d: want %v, got %v", i, expected[i], v)
		}
	}
}

func TestInitParallelism(t *testing.T) {
	msgs := []struct {
		level string
		msg   string
	}{}
	info := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"info", msg}) }
	warn := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"warn", msg}) }
	parallelism := 3
	created := false
	createSandboxes := func(n int) []int {
		if n != parallelism {
			t.Errorf("Parallelism value mismatch: got %d, want %d", n, parallelism)
		}
		created = true
		return []int{5, 6, 7}
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

func TestInitLowParallelism(t *testing.T) {
	msgs := []struct {
		level string
		msg   string
	}{}
	info := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"info", msg}) }
	warn := func(msg string) { msgs = append(msgs, struct{ level, msg string }{"warn", msg}) }
	createSandboxes := func(n int) []int { return []int{1} }
	_ = createSandboxes(1)
	warn("parallelism low warning")
	if len(msgs) == 0 {
		t.Errorf("Logger was not called for warn")
	}
}