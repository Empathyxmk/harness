package original

import (
	"encoding/json"
	"os"
	"testing"
)

type UploadTask struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Result struct {
		Form struct {
			Action string            `json:"action"`
			Fields map[string]string `json:"fields"`
		} `json:"form"`
	} `json:"result"`
}

func loadUploadTaskSample(t *testing.T) UploadTask {
	f, err := os.Open("../../tests/unit/responses/upload_task_created.json")
	if err != nil {
		t.Fatalf("Failed to open upload_task_created.json: %v", err)
	}
	defer f.Close()
	var task UploadTask
	dec := json.NewDecoder(f)
	if err := dec.Decode(&task); err != nil {
		t.Fatalf("JSON decode error: %v", err)
	}
	return task
}

func TestUploadTaskFields(t *testing.T) {
	task := loadUploadTaskSample(t)
	if task.Result.Form.Action == "" {
		t.Errorf("Upload task 'action' should not be empty")
	}
	if len(task.Result.Form.Fields) == 0 {
		t.Errorf("Upload task 'fields' should not be empty")
	}
}