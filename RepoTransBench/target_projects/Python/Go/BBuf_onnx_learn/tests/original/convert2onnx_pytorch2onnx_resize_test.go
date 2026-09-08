package original

import (
	"testing"
	"bbuf_onnx_learn/convert2onnx"
	"reflect"
)

func TestDummyResizeFunc(t *testing.T) {
	if got := convert2onnx.DummyResizeFunc(4, 5); !reflect.DeepEqual(got, [2]interface{}{4, 5}) {
		t.Errorf("DummyResizeFunc(4,5) = %v; want [4 5]", got)
	}
	if got := convert2onnx.DummyResizeFunc("x", 42); !reflect.DeepEqual(got, [2]interface{}{"x", 42}) {
		t.Errorf("DummyResizeFunc(\"x\",42) = %v; want [\"x\" 42]", got)
	}
}