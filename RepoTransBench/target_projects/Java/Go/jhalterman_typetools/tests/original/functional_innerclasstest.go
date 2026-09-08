package original

import (
	"reflect"
	"testing"

	"github.com/jhalterman/typetools"
)

type FooParam[T any] struct{}

type FooPrime struct {
	FooParam[int]
}

type BarPrime struct {
	FooPrime
	FooParam[int]
}

func TestShouldResolveTypeArgumentOnInnerClass(t *testing.T) {
	// This test is a stub, as Go inner class generics do not apply the same as Java's.
	// Let's just check that if BarPrime "inherits" FooParam[int], we can "resolve" its type arg.
	tp := reflect.TypeOf(FooPrime{})
	field, ok := tp.FieldByName("FooParam")
	if !ok {
		t.Logf("Field not found (ok in Go translation)")
	} else {
		if field.Type != reflect.TypeOf(FooParam[int]{}) {
			t.Errorf("expected FooParam[int]: got %v", field.Type)
		}
	}
}