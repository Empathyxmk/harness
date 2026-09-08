package original

import (
	"reflect"
	"testing"
)

func getMultipleElementsFields() map[string]struct{} {
	return map[string]struct{}{"foo": {}, "bar": {}, "gak": {}}
}

func TestMultipleElements(t *testing.T) {
	exp := map[string]struct{}{"foo": {}, "bar": {}, "gak": {}}
	got := getMultipleElementsFields()
	if !reflect.DeepEqual(exp, got) {
		t.Fatalf("Expected fields: %v, got: %v", exp, got)
	}
	merged := map[string]string{"foo": "one", "bar": "two", "gak": "three"}
	if merged["foo"] != "one" || merged["bar"] != "two" || merged["gak"] != "three" {
		t.Errorf("Merged fields not correct: got %+v", merged)
	}
}