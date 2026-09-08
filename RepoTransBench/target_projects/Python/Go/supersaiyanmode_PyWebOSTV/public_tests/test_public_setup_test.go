package public_tests

import (
	"encoding/json"
	"github.com/supersaiyanmode_PyWebOSTV/tests/original"
	"testing"
)

func TestPublicQueuePutAndGet(t *testing.T) {
	q := original.NewQueue()
	val := map[string]interface{}{"test": 99}
	q.Put(val)
	got, err := q.Get(true, 1.0)
	if err != nil {
		t.Fatalf("Get() error: %v", err)
	}
	gotmsg, ok := got.(map[string]interface{})
	if !ok || gotmsg["test"] != float64(99) {
		t.Errorf("Unexpected queue value: %v", got)
	}
}

func TestPublicQueueGetEmpty(t *testing.T) {
	q := original.NewQueue()
	_, err := q.Get(false, 0)
	if err == nil {
		t.Error("Expected error for empty queue, got nil")
	}
}

func TestPublicMessageMarshalUnmarshal(t *testing.T) {
	msg := original.Message{"a": "b", "n": 42}
	data, err := json.Marshal(msg)
	if err != nil {
		t.Fatalf("Marshal error: %v", err)
	}
	var got original.Message
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("Unmarshal error: %v", err)
	}
	if got["a"] != "b" || got["n"] != float64(42) {
		t.Errorf("Roundtrip mismatch: got %v", got)
	}
}