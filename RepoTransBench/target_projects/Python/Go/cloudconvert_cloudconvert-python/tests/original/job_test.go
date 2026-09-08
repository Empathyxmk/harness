package original

import (
	"fmt"
	"strings"
	"testing"
)

type Job map[string]interface{}

func NewJob(data map[string]interface{}) Job {
	return Job(data)
}

func (j Job) String() string {
	var b strings.Builder
	for k, v := range j {
		b.WriteString(fmt.Sprintf("%v: %v ", k, v))
	}
	return b.String()
}

func TestJobFromData(t *testing.T) {
	data := map[string]interface{}{"id": "abc", "status": "waiting"}
	j := NewJob(data)
	if j["id"] != "abc" {
		t.Errorf("Job.id expected 'abc', got %v", j["id"])
	}
	if j["status"] != "waiting" {
		t.Errorf("Job.status expected 'waiting', got %v", j["status"])
	}
}

func TestJobStrRepr(t *testing.T) {
	d := map[string]interface{}{"id": "a", "foo": "b"}
	j := NewJob(d)
	s := j.String()
	if !strings.Contains(s, "id") || !strings.Contains(s, "foo") {
		t.Errorf("Expected id and foo keys in Job string: %v", s)
	}
}

func TestJobFailMissingKey(t *testing.T) {
	j := NewJob(map[string]interface{}{})
	if len(j) != 0 {
		t.Errorf("Job should allow missing keys, got %v", j)
	}
}