package original

import "testing"

type Trackable interface {
	GetTrackableAttributes() map[string]interface{}
}

type DummyTrackable struct{}

func (DummyTrackable) GetTrackableAttributes() map[string]interface{} {
	return map[string]interface{}{"key": "val"}
}

func TestTrackableMethod(t *testing.T) {
	tbl := DummyTrackable{}
	attrs := tbl.GetTrackableAttributes()
	if len(attrs) != 1 || attrs["key"] != "val" {
		t.Fatalf("Expected {'key': 'val'}, got: %v", attrs)
	}
}