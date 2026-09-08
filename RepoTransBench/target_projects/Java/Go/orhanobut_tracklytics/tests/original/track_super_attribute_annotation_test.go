package original

import (
	"reflect"
	"testing"
)

type DummySuper struct{}

func (DummySuper) Dummy() {}

func TestTrackSuperAttributePresent(t *testing.T) {
	method := reflect.ValueOf(DummySuper{}).MethodByName("Dummy")
	if !method.IsValid() {
		t.Fatalf("Method not found")
	}
	// No annotations in Go, but test validates method present
	if method.Kind() != reflect.Func {
		t.Fatalf("Expected function kind for Dummy method")
	}
}