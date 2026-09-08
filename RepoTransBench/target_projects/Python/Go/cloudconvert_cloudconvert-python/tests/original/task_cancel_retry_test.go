package original

import (
	"encoding/json"
	"os"
	"testing"
)

type Task struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Status string `json:"status"`
	Tries  int    `json:"tries"`
}

func loadTaskRetrySample(t *testing.T) Task {
	f, err := os.Open("../../tests/unit/responses/retry.json")
	if err != nil {
		t.Fatalf("Failed to open retry.json: %v", err)
	}
	defer f.Close()
	var task Task
	dec := json.NewDecoder(f)
	if err := dec.Decode(&task); err != nil {
		t.Fatalf("JSON decode error: %v", err)
	}
	return task
}

func TestTaskCancelledStatus(t *testing.T) {
	task := loadTaskRetrySample(t)
	if task.Status != "canceled" && task.Status != "cancelled" {
		t.Errorf("Expected Status 'canceled' or 'cancelled', got '%s'", task.Status)
	}
}

func TestTaskRetryFields(t *testing.T) {
	task := loadTaskRetrySample(t)
	if task.Tries < 1 {
		t.Errorf("Task should have at least one try, got %d", task.Tries)
	}
	if task.ID == "" || task.Name == "" {
		t.Errorf("Task should have non-empty id and name fields")
	}
}