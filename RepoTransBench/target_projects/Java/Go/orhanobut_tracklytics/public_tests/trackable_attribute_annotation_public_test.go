package public_tests

import (
	"reflect"
	"testing"
)

type SamplePublic struct{}

func (SamplePublic) Sample(country string) {}

func TestTrackableAttributeAnnotationOnMethodPublic(t *testing.T) {
	m, ok := reflect.TypeOf(SamplePublic{}).MethodByName("Sample")
	if !ok {
		t.Fatalf("Sample method not found")
	}
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected Sample to be a function kind")
	}
}

func TestTrackableAttributeAnnotationOnParameterPublic(t *testing.T) {
	m, ok := reflect.TypeOf(SamplePublic{}).MethodByName("Sample")
	if !ok {
		t.Fatalf("Sample method not found")
	}
	if m.Type.NumIn() != 2 {
		t.Fatalf("Sample should have receiver and 1 param, got %d", m.Type.NumIn())
	}
}