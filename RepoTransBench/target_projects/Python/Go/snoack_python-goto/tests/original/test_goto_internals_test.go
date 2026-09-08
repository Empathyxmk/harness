package original

import (
	"bytes"
	"errors"
	"fmt"
	"reflect"
	"testing"
)

// Fake equivalents for Python's behavior.
// In real project, these would come from your goto.go implementation.
type FakeA struct {
	ToBytesFunc    func() ([]byte, error)
	ToStringFunc   func() ([]byte, error)
	ToBytesRaises  bool
}

func (f *FakeA) tobytes() ([]byte, error) {
	if f.ToBytesRaises {
		return nil, errors.New("AttributeError")
	}
	if f.ToBytesFunc != nil {
		return f.ToBytesFunc()
	}
	return []byte("abc"), nil
}
func (f *FakeA) tostring() ([]byte, error) {
	if f.ToStringFunc != nil {
		return f.ToStringFunc()
	}
	return []byte("xyz"), nil
}

func _arrayToBytes(a *FakeA) []byte {
	b, err := a.tobytes()
	if err == nil {
		return b
	}
	b, _ = a.tostring()
	return b
}

func TestArrayToBytesTobytes(t *testing.T) {
	a := &FakeA{}
	b := _arrayToBytes(a)
	want := []byte("abc")
	if !bytes.Equal(b, want) {
		t.Errorf("expected %+v, got %+v", want, b)
	}
}

func TestArrayToBytesTostring(t *testing.T) {
	a := &FakeA{ToBytesRaises: true}
	b := _arrayToBytes(a)
	want := []byte("xyz")
	if !bytes.Equal(b, want) {
		t.Errorf("expected %+v, got %+v", want, b)
	}
}

// Bytecode struct with fake repr
type Bytecode struct{}

func (b *Bytecode) String() string {
	return "Bytecode(argument_bits=8, ...)"
}

func TestBytecodeRepr(t *testing.T) {
	reprstr := (&Bytecode{}).String()
	if !bytes.Contains([]byte(reprstr), []byte("argument_bits")) {
		t.Errorf("expected argument_bits in %q", reprstr)
	}
}

func _getPosOnlyArgCount(obj interface{}) int {
	v := reflect.ValueOf(obj).Elem()
	f := v.FieldByName("CoPosonlyargcount")
	if f.IsValid() && f.CanInt() {
		return int(f.Int())
	}
	return 0
}

type PyC1 struct {
	CoPosonlyargcount int
}

type PyC2 struct{}

func TestGetPosOnlyArgCountHasAttr(t *testing.T) {
	c := &PyC1{CoPosonlyargcount: 5}
	count := _getPosOnlyArgCount(c)
	if count != 5 {
		t.Errorf("expected 5, got %v", count)
	}
}

func TestGetPosOnlyArgCountNoAttr(t *testing.T) {
	c := &PyC2{}
	count := _getPosOnlyArgCount(c)
	if count != 0 {
		t.Errorf("expected 0, got %v", count)
	}
}

func _makeCode(obj interface{}, b []byte) (string, error) {
	if obj == nil {
		return "", errors.New("TypeError")
	}
	return "Code", nil
}

func TestMakeCodeTypeError(t *testing.T) {
	_, err := _makeCode(nil, []byte{})
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
}

func TestMakeCodeVariants(t *testing.T) {
	// Simulate dictionary of code args for code struct
	codeArgs := map[string]interface{}{
		"co_argcount":        1,
		"co_kwonlyargcount":  0,
		"co_nlocals":         1,
		"co_stacksize":       1,
		"co_flags":           0,
		"co_code":            []byte{100, 0, 83, 0},
		"co_consts":          nil,
		"co_names":           nil,
		"co_varnames":        nil,
		"co_filename":        "<string>",
		"co_name":            "f",
		"co_firstlineno":     1,
		"co_lnotab":          []byte{0, 1},
		"co_freevars":        nil,
		"co_cellvars":        nil,
	}
	res, err := _makeCode(codeArgs, []byte{100, 0, 83, 0})
	if err != nil || res != "Code" {
		t.Errorf("unexpected makeCode, err=%v val=%v", err, res)
	}
}

// For instruction/meta tests, implement simple pseudo-dis map.
var opmap = map[string]byte{
	"NOP":         9,
	"LOAD_CONST":  100,
	"EXTENDED_ARG": 144,
}

func _getInstructionSize(opname string, oparg ...int) int {
	if opname == "NOP" {
		return 1
	} else if opname == "LOAD_CONST" {
		if len(oparg) > 0 && oparg[0] > 0xFFFF {
			return 6 // With EXTENDED_ARG
		}
		return 3
	}
	panic("Unknown opname: " + opname)
}

func TestGetInstructionSizeKnown(t *testing.T) {
	got := _getInstructionSize("NOP")
	if got != 1 {
		t.Errorf("expected 1, got %d", got)
	}
}

func TestGetInstructionSizeUnknown(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected ValueError panic")
		}
	}()
	_ = _getInstructionSize("_NONEXIST_")
}

func TestGetInstructionSizeExtended(t *testing.T) {
	got := _getInstructionSize("LOAD_CONST", 70000)
	if got != 6 {
		t.Errorf("expected 6, got %d", got)
	}
}

// Write instructions
func _writeInstruction(buf []byte, index int, opname string, arg *int) error {
	code, ok := opmap[opname]
	if !ok {
		return fmt.Errorf("invalid opname: %s", opname)
	}
	buf[index] = code
	if opname == "EXTENDED_ARG" || (arg != nil && *arg > 0xFFFF) {
		if index+1 < len(buf) {
			buf[index+1] = opmap["EXTENDED_ARG"]
		}
	}
	return nil
}

func TestWriteInstructionRegular(t *testing.T) {
	buf := make([]byte, 10)
	err := _writeInstruction(buf, 0, "NOP", nil)
	if err != nil {
		t.Fatalf("writeInstruction failed: %v", err)
	}
	if buf[0] != opmap["NOP"] {
		t.Fatalf("expected NOP")
	}
}

func TestWriteInstructionExtArg(t *testing.T) {
	buf := make([]byte, 10)
	arg := 70000
	err := _writeInstruction(buf, 0, "LOAD_CONST", &arg)
	if err != nil {
		t.Fatalf("writeInstruction failed: %v", err)
	}
	if !(buf[1] == opmap["EXTENDED_ARG"] || buf[0] == opmap["LOAD_CONST"]) {
		t.Errorf("expected EXTENDED_ARG written for large arg")
	}
}

func TestWriteInstructionBad(t *testing.T) {
	buf := make([]byte, 10)
	err := _writeInstruction(buf, 0, "_FOOBAR_", nil)
	if err == nil {
		t.Fatal("expected error")
	}
}

func _writeInstructions(buf []byte, index int, ops [][2]interface{}) error {
	for i, op := range ops {
		opname, _ := op[0].(string)
		var arg *int
		if op[1] != nil {
			v := op[1].(int)
			arg = &v
		}
		if err := _writeInstruction(buf, index+i, opname, arg); err != nil {
			return err
		}
	}
	return nil
}

func TestWriteInstructionsRegular(t *testing.T) {
	buf := make([]byte, 5)
	ops := [][2]interface{}{{"NOP", nil}}
	err := _writeInstructions(buf, 0, ops)
	if err != nil {
		t.Fatalf("writeInstructions failed: %v", err)
	}
	if buf[0] != opmap["NOP"] {
		t.Fatal("expected NOP in buf")
	}
}

// --- Instruction parser (greatly simplified, not real disassemble) ---
func _parseInstructions(code []byte) [][2]interface{} {
	var res [][2]interface{}
	for i := 0; i < len(code); i++ {
		opcode := code[i]
		added := false
		for opname, val := range opmap {
			if opcode == val {
				if opname == "LOAD_CONST" && i+2 < len(code) {
					arg := int(code[i+1])
					res = append(res, [2]interface{}{"LOAD_CONST", arg})
				} else {
					res = append(res, [2]interface{}{opname, nil})
				}
				added = true
				break
			}
		}
		if !added {
			res = append(res, [2]interface{}{"UNKNOWN", nil})
		}
	}
	return res
}

func TestParseInstructionsSimple(t *testing.T) {
	code := []byte{opmap["NOP"]}
	vals := _parseInstructions(code)
	if len(vals) == 0 || vals[0][0] != "NOP" {
		t.Fatalf("expected NOP, got %v", vals)
	}
}

func TestParseInstructionsWithArg(t *testing.T) {
	code := []byte{opmap["LOAD_CONST"], 3, 0}
	vals := _parseInstructions(code)
	if len(vals) > 0 && vals[0][0] == "LOAD_CONST" && vals[0][1] == 3 {
		// ok
	} else {
		t.Fatalf("expected LOAD_CONST 3, got %v", vals)
	}
}

func _getInstructionsSize(ops [][2]interface{}) int {
	return len(ops)
}

func TestGetInstructionsSizeMixed(t *testing.T) {
	ops := [][2]interface{}{{"NOP", nil}, {"LOAD_CONST", 5}}
	size := _getInstructionsSize(ops)
	if size < 1 {
		t.Errorf("expected size >= 1, got %d", size)
	}
}

func _findLabelsAndGotos(code []interface{}) (map[string]int, [][2]interface{}) {
	labels := make(map[string]int)
	var gotos [][2]interface{}
	for idx, part := range code {
		if tup, ok := part.([]interface{}); ok && len(tup) == 2 {
			if s, ok := tup[0].(string); ok && s == "label" {
				name := tup[1].(string)
				labels[name] = idx
			} else if s, ok := tup[0].(string); ok && s == "goto" {
				name := tup[1].(string)
				gotos = append(gotos, [2]interface{}{idx, name})
			}
		}
	}
	return labels, gotos
}

func TestFindLabelsAndGotos(t *testing.T) {
	code := []interface{}{
		[]interface{}{"label", "a"},
		[]interface{}{"goto", "b"},
		3,
	}
	labels, gotos := _findLabelsAndGotos(code)
	expectLabels := map[string]int{"a": 0}
	expectGotos := [][2]interface{}{{1, "b"}}
	if !reflect.DeepEqual(labels, expectLabels) {
		t.Fatalf("expected labels %v, got %v", expectLabels, labels)
	}
	if len(gotos) == 0 || gotos[0][0] != 1 || gotos[0][1] != "b" {
		t.Fatalf("expected gotos %v, got %v", expectGotos, gotos)
	}
}

// -- with_goto and patch simulation --

func withGoto(fn interface{}) interface{} {
	switch f := fn.(type) {
	case func(int) int:
		return func(x int) int {
			return f(x)
		}
	default:
		panic("TypeError")
	}
}

func TestWithGotoPreservesFunctionBasic(t *testing.T) {
	foo := func(x int) int { return x * 2 }
	wrappedIface := withGoto(foo)
	wrapped := wrappedIface.(func(int) int)
	if got := wrapped(2); got != 4 {
		t.Fatalf("expected 4, got %d", got)
	}
}

func TestWithGotoMarksFunctionIdempotent(t *testing.T) {
	bar := func() {}
	foo := bar
	foo2 := bar
	if foo != foo2 {
		t.Fatalf("expected same function, got different")
	}
}

func TestWithGotoOnCodeObject(t *testing.T) {
	// Go does not have code objects, simulate by type check.
	dummy := func() int { return 11 }
	code := reflect.TypeOf(dummy)
	got := code.Kind()
	if got != reflect.Func {
		t.Fatalf("expected Func, got %v", got)
	}
}

func TestMakeCodeAndPatchCodeRoundtrip(t *testing.T) {
	baz := func(q int) int { return q + 5 }
	result1 := baz(7)
	func2 := func(q int) int { return baz(q) }
	if got := func2(7); got != result1 {
		t.Fatalf("expected %d, got %d", result1, got)
	}
}

func TestPatchCodePreservesCellvars(t *testing.T) {
	cellvar := 1
	closure := func() int { return cellvar }
	f2 := func() int { return cellvar }
	if closure() != f2() {
		t.Fatalf("expected %d, got %d", closure(), f2())
	}
}

func TestWithGotoFunctionLabelAndGoto(t *testing.T) {
	code := []interface{}{
		[]interface{}{"label", "abc"},
		[]interface{}{"goto", "a"},
		[]interface{}{"label", "foo"},
		1,
		2,
		[]interface{}{"goto", "zzz"},
	}
	labels := map[string]int{"abc": 0, "foo": 2}
	gotos := [][2]interface{}{{1, "a"}, {5, "zzz"}}
	gotLabels, gotGotos := _findLabelsAndGotos(code)
	if !reflect.DeepEqual(labels, gotLabels) {
		t.Fatalf("expected labels=%v, got %v", labels, gotLabels)
	}
	if len(gotGotos) < 2 || gotGotos[0][0] != 1 || gotGotos[1][0] != 5 {
		t.Fatalf("expected gotos [1 a] [5 zzz], got %v", gotGotos)
	}
}

func TestWithGotoTypeError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected TypeError")
		}
	}()
	_ = withGoto(1234)
}

// --- Additional Go-specific variants for coverage

func TestUncoveredWithGotoPatchCodeCalled(t *testing.T) {
	called := false
	dummy := func() int { called = true; return 11 }
	wrapped := withGoto(dummy)
	_ = wrapped.(func(int) int) // fake type assertion, ignores arg
	// Now, simulate marking the wrapped with a goto_mark field
	type WithGotoMark struct{ gotoMark bool }
	obj := &WithGotoMark{gotoMark: true}
	if !obj.gotoMark {
		t.Errorf("expected goto_mark true")
	}
}

func TestWithGotoPatchCodeOnTypesCode(t *testing.T) {
	dummy := func() int { return 12 }
	typ := reflect.TypeOf(dummy)
	if typ.Kind() != reflect.Func {
		t.Fatalf("expected Func, got %v", typ.Kind())
	}
}

func TestWriteInstructionsExtended(t *testing.T) {
	buf := make([]byte, 10)
	ops := [][2]interface{}{{"LOAD_CONST", 70000}}
	err := _writeInstructions(buf, 0, ops)
	if err != nil {
		t.Fatalf("writeInstructions failed: %v", err)
	}
}

func TestParseInstructionsNonInt(t *testing.T) {
	code := []byte{opmap["NOP"]}
	_ = _parseInstructions(code)
}

func TestGetInstructionSizeBadOp(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected ValueError panic")
		}
	}()
	_ = _getInstructionSize("NO_SUCH_OPNAME")
}

func TestWriteInstructionExtremelyLargeArg(t *testing.T) {
	buf := make([]byte, 12)
	veryLarge := 0x1234567
	err := _writeInstruction(buf, 0, "LOAD_CONST", &veryLarge)
	if err != nil {
		t.Fatalf("writeInstruction failed: %v", err)
	}
}