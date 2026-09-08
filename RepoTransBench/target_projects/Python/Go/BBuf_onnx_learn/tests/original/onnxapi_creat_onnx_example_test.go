package original

import (
	"testing"
	"bbuf_onnx_learn/onnxapi"
	"reflect"
)

func TestMakeIdentity(t *testing.T) {
	if got := onnxapi.MakeIdentity(100); got != 100 {
		t.Errorf("MakeIdentity(100) = %v; want 100", got)
	}
	input := []int{1, 2, 3}
	got := onnxapi.MakeIdentity(input)
	// Must use reflect.DeepEqual for slices
	if !reflect.DeepEqual(got, input) {
		t.Errorf("MakeIdentity([1,2,3]) = %v; want [1,2,3]", got)
	}
}

func TestSumList(t *testing.T) {
	list := []int{1, 2, 3}
	if got := onnxapi.SumList(list); got != 6 {
		t.Errorf("SumList([1,2,3]) = %v; want 6", got)
	}
	empty := []int{}
	if got := onnxapi.SumList(empty); got != 0 {
		t.Errorf("SumList([]) = %v; want 0", got)
	}
}