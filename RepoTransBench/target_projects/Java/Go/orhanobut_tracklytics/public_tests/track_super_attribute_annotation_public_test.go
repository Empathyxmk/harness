package public_tests

import (
	"reflect"
	"testing"
)

type SuperPublic struct{}

func (SuperPublic) PublicDummy() {}

func TestTrackSuperAttributePresentPublic(t *testing.T) {
	m, ok := reflect.TypeOf(SuperPublic{}).MethodByName("PublicDummy")
	if !ok {
		t.Fatalf("Expected PublicDummy method")
	}
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected a function kind for PublicDummy")
	}
}