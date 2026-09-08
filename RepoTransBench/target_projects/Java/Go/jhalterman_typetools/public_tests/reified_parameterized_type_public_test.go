package public_tests

import (
	"reflect"
	"strings"
	"testing"

	"github.com/jhalterman/typetools"
)

type PublicSample[X, Y any] struct{}

type PublicSampleHolder struct {
	sample PublicSample[float64, rune]
}

func getParameterizedType() reflect.Type {
	return reflect.TypeOf(PublicSample[float64, rune]{})
}

func TestAddReifiedTypeArgument_Normal_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	rpt.AddReifiedTypeArgument(reflect.TypeOf('a'))

	args := rpt.GetActualTypeArguments()
	if args[0] != reflect.TypeOf(0.0) {
		t.Errorf("First type argument should be float64")
	}
	if args[1] != reflect.TypeOf('a') {
		t.Errorf("Second type argument should be rune")
	}
}

func TestAddReifiedTypeArgument_Loop_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(rpt)
	rpt.AddReifiedTypeArgument(reflect.TypeOf('a'))

	args := rpt.GetActualTypeArguments()
	if args[0] != rpt {
		t.Errorf("First type argument should be self (loop)")
	}
	if args[1] != reflect.TypeOf('a') {
		t.Errorf("Second type argument should be rune")
	}
	str := rpt.ToString()
	if !strings.Contains(str, "...") {
		t.Errorf("toString does not contain ... for self-loop, got: %s", str)
	}
}

func TestAddReifiedTypeArgument_Overflow_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	rpt.AddReifiedTypeArgument(reflect.TypeOf('a'))
	rpt.AddReifiedTypeArgument(reflect.TypeOf(float32(0))) // Should be ignored

	args := rpt.GetActualTypeArguments()
	if len(args) > 2 {
		t.Errorf("More than two arguments present: %+v", args)
	}
}

func TestToString_OwnerType_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	rpt.AddReifiedTypeArgument(nil)
	rpt.AddReifiedTypeArgument(reflect.TypeOf('a'))
	str := rpt.ToString()
	if !strings.Contains(str, "null") {
		t.Errorf("Null type argument not present in string: %s", str)
	}
	if !strings.Contains(str, reflect.TypeOf('a').String()) {
		t.Errorf("Rune type argument not present in string: %s", str)
	}
}

func TestEquals_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt1 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt2 := typetools.NewReifiedParameterizedType(pt, 2)

	rpt1.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	rpt1.AddReifiedTypeArgument(reflect.TypeOf('a'))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf('a'))
	if !rpt1.Equals(rpt2) || !rpt2.Equals(rpt1) {
		t.Errorf("Equal ReifiedParameterizedType instances not recognized as such")
	}

	rpt3 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt3.AddReifiedTypeArgument(reflect.TypeOf('a'))
	rpt3.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	if rpt1.Equals(rpt3) {
		t.Errorf("Different type arguments should not be equal")
	}
}

func TestHashCode_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt1 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt2 := typetools.NewReifiedParameterizedType(pt, 2)
	rpt1.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	rpt1.AddReifiedTypeArgument(reflect.TypeOf('a'))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf(0.0))
	rpt2.AddReifiedTypeArgument(reflect.TypeOf('a'))
	if rpt1.HashCode() != rpt2.HashCode() {
		t.Errorf("Hash codes for equal should match")
	}
}

func TestNotEquals_DifferentType_Public(t *testing.T) {
	pt := getParameterizedType()
	rpt := typetools.NewReifiedParameterizedType(pt, 2)
	if rpt.Equals(nil) {
		t.Errorf("Equals(nil) should be false")
	}
}