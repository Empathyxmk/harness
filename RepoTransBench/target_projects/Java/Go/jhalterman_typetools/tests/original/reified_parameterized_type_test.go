package original

import (
	"reflect"
	"strings"
	"testing"

	"github.com/jhalterman/typetools"
)

type Sample[A, B any] struct{}

type SampleHolder struct {
	sample Sample[string, int]
}

func getParameterizedType() reflect.Type {
	return reflect.TypeOf(Sample[string, int]{})
}

func TestAddReifiedTypeArgument_Normal(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(reflect.TypeOf(""))
	rpt.AddReifiedTypeArgument(reflect.TypeOf(0))

	args := rpt.GetActualTypeArguments()
	if args[0] != reflect.TypeOf("") {
		t.Errorf("First type argument should be string")
	}
	if args[1] != reflect.TypeOf(0) {
		t.Errorf("Second type argument should be int")
	}
}

func TestAddReifiedTypeArgument_Loop(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(rpt)
	rpt.AddReifiedTypeArgument(reflect.TypeOf(0))

	args := rpt.GetActualTypeArguments()
	if args[0] != rpt {
		t.Errorf("First type argument should be self (loop)")
	}
	if args[1] != reflect.TypeOf(0) {
		t.Errorf("Second type argument should be int")
	}
	str := rpt.ToString()
	if !strings.Contains(str, "...") {
		t.Errorf("toString does not contain ... for self-loop, got: %s", str)
	}
}

func TestAddReifiedTypeArgument_Overflow(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(reflect.TypeOf(""))
	rpt.AddReifiedTypeArgument(reflect.TypeOf(0))
	rpt.AddReifiedTypeArgument(reflect.TypeOf(true)) // Should be ignored

	args := rpt.GetActualTypeArguments()
	if len(args) > 2 {
		t.Errorf("More than two arguments present: %+v", args)
	}
}

func TestToString_OwnerType(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(nil)
	rpt.AddReifiedTypeArgument(reflect.TypeOf(0))
	str := rpt.ToString()
	if !strings.Contains(str, "null") {
		t.Errorf("Null type argument not present in string: %s", str)
	}
	if !strings.Contains(str, reflect.TypeOf(0).String()) {
		t.Errorf("Int type argument not present in string: %s", str)
	}
}

func TestEquals(t *testing.T) {
	pt := getParameterizedType()
	rpt1 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt2 := typetools.NewReifiedParameterizedType(pt, 2)

	rpt1.AddReifiedTypeArgument(reflect.TypeOf(""))
	rpt1.AddReifiedTypeArgument(reflect.TypeOf(0))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf(""))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf(0))
	if !rpt1.Equals(rpt2) || !rpt2.Equals(rpt1) {
		t.Errorf("Equal ReifiedParameterizedType instances not recognized as such")
	}

	rpt3 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt3.AddReifiedTypeArgument(reflect.TypeOf(0))
	rpt3.AddReifiedTypeArgument(reflect.TypeOf(""))
	if rpt1.Equals(rpt3) {
		t.Errorf("Different type arguments should not be equal")
	}
}

func TestHashCode(t *testing.T) {
	pt := getParameterizedType()
	rpt1 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt2 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt1.AddReifiedTypeArgument(reflect.TypeOf(""))
	rpt1.AddReifiedTypeArgument(reflect.TypeOf(0))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf(""))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf(0))
	if rpt1.HashCode() != rpt2.HashCode() {
		t.Errorf("Hash codes for equal should match")
	}
}

func TestNotEquals_DifferentType(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	if rpt.Equals(nil) {
		t.Errorf("Equals(nil) should be false")
	}
}