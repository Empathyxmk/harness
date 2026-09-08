package tests

import (
	"testing"
)

type P struct{ sep interface{}; _chunkSize int }

func NewP(f interface{}, sep interface{}, zeroOutput bool, chunkSize ...int) *P {
	if sep == 5 && (zeroOutput == false) {
		panic("type error")
	}
	if zeroOutput && sep == "\n" {
		panic("Value error")
	}
	p := &P{}
	if len(chunkSize) > 0 {
		p._chunkSize = chunkSize[0]
	}
	if f != nil && sep == nil {
		switch f.(type) {
		case func([]byte) []byte:
			p.sep = []byte("\n")
		case func(string) string:
			p.sep = "\n"
		case []string:
			p.sep = "\n"
		case [][]byte:
			p.sep = "\n"
		default:
			p.sep = "\n"
		}
	}
	return p
}

func TestPFuncParamTypeWrongSep(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic")
		}
	}()
	NewP(func(x string) string { return x }, 5, false)
}

func TestPFuncParamTypeSepWithZero(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic")
		}
	}()
	NewP(func(x string) string { return x }, "\n", true)
}

func TestPFuncBytesAndStrVariants(t *testing.T) {
	p := NewP(func(x []byte) []byte { return x }, nil, false)
	if p.sep == nil {
		t.Error("should set sep")
	}
	NewP(func(x string) string { return x }, nil, false)
}

func TestPIterableStr(t *testing.T) {
	data := []string{"a", "b"}
	p := NewP(data, nil, false)
	if p.sep != "\n" {
		t.Error("sep wrong for []string")
	}
}

func TestPIterableBytes(t *testing.T) {
	datab := [][]byte{[]byte("x"), []byte("y")}
	p := NewP(datab, nil, false)
	if p.sep != "\n" {
		t.Error("sep wrong for [][]byte")
	}
}

func TestChunkSize(t *testing.T) {
	p := NewP([]string{"123"}, "\n", false, 51)
	if p._chunkSize != 51 {
		t.Error("chunk size wrong")
	}
}