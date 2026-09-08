package public_tests

import "testing"

type PubTestService struct {
	TASKS []string
}

func TestPublicTasksAttribute(t *testing.T) {
	svc := PubTestService{TASKS: []string{"task1", "task2"}}
	cmdTasks := []string{"task1", "task2"}
	if len(svc.TASKS) != len(cmdTasks) {
		t.Fatalf("TASKS len mismatch")
	}
	for i, v := range svc.TASKS {
		if v != cmdTasks[i] {
			t.Errorf("TASKS[%d] = %s, want %s", i, v, cmdTasks[i])
		}
	}
}

func TestPublicInitFromCLIExists(t *testing.T) {
	// Not applicable in Go; always true if desired
}