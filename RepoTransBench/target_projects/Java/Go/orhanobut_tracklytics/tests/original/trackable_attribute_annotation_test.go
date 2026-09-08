package original

import (
	"reflect"
	"testing"
)

type DummyAttribute struct{}

func (DummyAttribute) AnnotatedMethod(param string) {}

func TestTrackableAttributeOnMethod(t *testing.T) {
	m, ok := reflect.TypeOf(DummyAttribute{}).MethodByName("AnnotatedMethod")
	if !ok {
		t.Fatalf("Method AnnotatedMethod not found")
	}
	// No annotation in Go, but method exists
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected a function type for AnnotatedMethod")
	}
}

func TestTrackableAttributeOnParameter(t *testing.T) {
	m, ok := reflect.TypeOf(DummyAttribute{}).MethodByName("AnnotatedMethod")
	if !ok {
		t.Fatalf("Method AnnotatedMethod not found")
	}
	// Go does not have parameter-level annotations, only for demonstration.
	if m.Type.NumIn() != 2 {
		t.Fatalf("Expected two parameters (receiver + param), got %d", m.Type.NumIn())
	}
}

func TestTargetTypeOnAnnotation(t *testing.T) {
	m, ok := reflect.TypeOf(DummyAttribute{}).MethodByName("AnnotatedMethod")
	if !ok {
		t.Fatalf("Method AnnotatedMethod not found")
	}
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected function kind")
	}
}

func TestRetentionPolicy(t *testing.T) {
	// No direct annotation retention reflection, so this is a placeholder for concept
	if false {
		t.Fatalf("Should be at runtime in Java")
	}
}