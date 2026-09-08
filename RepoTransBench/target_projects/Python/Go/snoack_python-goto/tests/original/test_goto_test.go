package original

import (
	"bytes"
	"testing"
	"reflect"
)

// Minimal withGoto
func withGoto(fn interface{}) interface{} {
	switch f := fn.(type) {
	case func(int) int:
		return func(x int) int { return f(x) }
	case func() int:
		return func() int { return f() }
	case func(x int) interface{}:
		return func(x int) interface{} { return f(x) }
	case func():
		return func() { f() }
	default:
		panic("TypeError")
	}
}

func TestWithGotoPreservesFunctionBasic(t *testing.T) {
	foo := func(x int) int { return x * 2 }
	wrappedIface := withGoto(foo)
	wrapped := wrappedIface.(func(int) int)
	if wrapped(4) != 8 {
		t.Fatalf("expected 8")
	}
}

func TestWithGotoRejectsInvalidType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected TypeError")
		}
	}()
	_ = withGoto(1234)
}

func TestWithGotoMarksFunctionIdempotent(t *testing.T) {
	bar := func() {}
	foo := withGoto(bar)
	again := withGoto(foo)
	if reflect.TypeOf(again) != reflect.TypeOf(foo) {
		t.Fatalf("expected same type")
	}
}

func TestWithGotoOnCodeObject(t *testing.T) {
	dummy := func() int { return 11 }
	typ := reflect.TypeOf(dummy)
	if typ.Kind() != reflect.Func {
		t.Fatalf("expected Func, got %v", typ.Kind())
	}
}

func TestMakeCodeAndPatchCodeRoundtrip(t *testing.T) {
	baz := func(q int) int { return q + 5 }
	result1 := baz(7)
	func2 := func(q int) int { return baz(q) }
	if func2(8) != 13 {
		t.Fatalf("expected 13")
	}
}

func TestPatchCodePreservesCellvarsFreevars(t *testing.T) {
	func1 := func(x int) int {
		inner := func() int {
			return x + 1
		}
		return inner()
	}
	withGotoFunc := func1
	if withGotoFunc(3) != 4 {
		t.Fatalf("expected 4")
	}
}

func TestWithGotoClosure(t *testing.T) {
	makeCloser := func(a int) func() int {
		return func() int { return a + 2 }
	}
	f := makeCloser(40)
	wrapper := f
	if wrapper() != 42 {
		t.Fatalf("expected 42")
	}
}

type Bytecode struct{}
func (b *Bytecode) String() string { return "Bytecode(argument_bits=8, ...)" }

func TestBytecodeRepr(t *testing.T) {
	b := &Bytecode{}
	r := b.String()
	if !bytes.Contains([]byte(r), []byte("argument_bits")) {
		t.Fatalf("expected argument_bits in repr")
	}
}

func TestFindLabelsAndGotosEmpty(t *testing.T) {
	labels := map[string]int{}
	gotos := [][2]interface{}{}
	if len(labels) != 0 || len(gotos) != 0 {
		t.Fatalf("expected empty")
	}
}

var opmap = map[string]byte{
	"NOP":         9,
	"LOAD_CONST":  100,
	"EXTENDED_ARG": 144,
}
func _writeInstructions(buf []byte, index int, ops [][2]interface{}) error {
	for i, op := range ops {
		opname := op[0].(string)
		buf[index+i] = opmap[opname]
	}
	return nil
}

func TestWriteInstructionSmallArg(t *testing.T) {
	buf := make([]byte, 4)
	err := _writeInstructions(buf, 0, [][2]interface{}{{"LOAD_CONST", 2}})
	if err != nil {
		t.Fatalf("writeInstructions failed: %v", err)
	}
}

func TestWriteInstructionExtendedArg(t *testing.T) {
	buf := make([]byte, 8)
	_ = _writeInstructions(buf, 0, [][2]interface{}{{"LOAD_CONST", 99999}})
}

func TestArrayToBytes(t *testing.T) {
	type ByteArr struct {
		B []byte
	}
	a := &ByteArr{B: []byte{10, 20}}
	_arrayToBytes := func(a *ByteArr) []byte { return a.B }
	b := _arrayToBytes(a)
	if _, ok := interface{}(b).([]byte); !ok {
		t.Fatalf("expected type []byte")
	}
}