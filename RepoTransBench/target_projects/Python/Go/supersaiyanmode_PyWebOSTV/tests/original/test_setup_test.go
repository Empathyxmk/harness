package original

import (
	"encoding/json"
	"testing"
)

// Test queue functionality with blocking get and timeout
func TestQueuePutAndGet(t *testing.T) {
	q := NewQueue()
	in := map[string]interface{}{"msg": 10}
	q.Put(in)
	got, err := q.Get(true, 1) // block, 1 second timeout
	if err != nil {
		t.Fatalf("Get() returned err: %v", err)
	}
	gotmsg, ok := got.(map[string]interface{})
	if !ok || gotmsg["msg"] != 10.0 {
		t.Errorf("Queue returned wrong msg: %v", got)
	}
}

// Test queue empty get returns error
func TestQueueGetEmpty(t *testing.T) {
	q := NewQueue()
	_, err := q.Get(false, 0)
	if err == nil {
		t.Error("Expected error for empty queue, got nil")
	}
}

// Test for JSON marshal/unmarshal round-trip in Message
func TestMessageMarshalUnmarshal(t *testing.T) {
	msg := Message{"foo": "bar", "count": 3}
	data, err := json.Marshal(msg)
	if err != nil {
		t.Fatalf("Marshal error: %v", err)
	}
	var got Message
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("Unmarshal error: %v", err)
	}
	if got["foo"] != "bar" || got["count"] != float64(3) {
		t.Errorf("Roundtrip mismatch: got %v", got)
	}
}