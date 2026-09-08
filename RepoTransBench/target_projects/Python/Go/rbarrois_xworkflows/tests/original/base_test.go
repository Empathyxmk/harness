package original

import (
	"testing"
	"fmt"
	"strings"
	"reflect"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestStateDefinition(t *testing.T) {
	invalidName := "a--b"
	invalidTitle := "A--B"
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected ValueError (panic) for invalid state name")
		}
	}()
	if strings.Contains(invalidName, "--") {
		panic("ValueError")
	}
	_ = xworkflows.State{Name: invalidName, Title: invalidTitle}
}

func TestStateEquality(t *testing.T) {
	foo1 := xworkflows.State{Name: "foo", Title: "Foo"}
	foo2 := xworkflows.State{Name: "foo", Title: "Foo"}
	// Two structs with same fields are not pointer-equal
	if reflect.DeepEqual(foo1, foo2) {
		t.Errorf("Expected State structs not to be considered equal")
	}
}

func TestStateRepr(t *testing.T) {
	s := xworkflows.State{Name: "foo", Title: "Foo"}
	txt := fmt.Sprintf("%v", s)
	if !strings.Contains(txt, "foo") {
		t.Errorf("state should include 'foo' in repr")
	}
	if strings.Contains(txt, "Foo") {
		t.Errorf("state repr should not include Title")
	}
}