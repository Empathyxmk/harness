package public_tests

import (
	"reflect"
	"testing"
)

type BarPublic struct{}

func (BarPublic) OnTracked(event interface{}) {}

func TestImplementsTrackablePublic(t *testing.T) {
	var b interface{} = BarPublic{}
	// Go doesn't have explicit implements check, but type assertion is okay
	if _, ok := b.(interface{ OnTracked(interface{}) }); !ok {
		t.Fatalf("BarPublic should implement OnTracked(Event) method")
	}
}

func TestOnTrackedMethodPresentPublic(t *testing.T) {
	m, ok := reflect.TypeOf(BarPublic{}).MethodByName("OnTracked")
	if !ok {
		t.Fatalf("OnTracked method not found on BarPublic")
	}
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("OnTracked should be a function kind")
	}
}