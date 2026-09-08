package public_tests

import (
	"testing"
	"bbuf_onnx_learn/onnxapi"
	"reflect"
)

func TestMakeIdentity(t *testing.T) {
	if got := onnxapi.MakeIdentity("hello"); got != "hello" {
		t.Errorf("MakeIdentity(\"hello\") = %v; want \"hello\"", got)
	}
	input := []int{7,8,9}
	got := onnxapi.MakeIdentity(input)
	if !reflect.DeepEqual(got, input) {
		t.Errorf("MakeIdentity([7,8,9]) = %v; want [7,8,9]", got)
	}
}

func TestSumList(t *testing.T) {
	list := []int{4,5,6}
	if got := onnxapi.SumList(list); got != 15 {
		t.Errorf("SumList([4,5,6]) = %v; want 15", got)
	}
	single := []int{100}
	if got := onnxapi.SumList(single); got != 100 {
		t.Errorf("SumList([100]) = %v; want 100", got)
	}
}