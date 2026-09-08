package public_tests

import "testing"

func TestPublicStrIsStr(t *testing.T) {
	var s interface{} = "a"
	if _, ok := s.(string); !ok {
		t.Error("Expected string to be a string")
	}
	if typ := typeof(""); typ != "string" {
		t.Errorf("Expected \"\" type to be string, got %v", typ)
	}
}

func TestPublicIntIsInt(t *testing.T) {
	y := 42
	if typeof(y) != "int" && typeof(y) != "int32" && typeof(y) != "int64" {
		t.Errorf("Expected int, got %v", typeof(y))
	}
}

func TestPublicUnicodeIsStrPy3(t *testing.T) {
	z := "foo"
	if typeof(z) != "string" {
		t.Error("Expected unicode to be string type")
	}
}

func TestPublicPy3Features(t *testing.T) {
	s := "format: %s"
	if !(len(s) > 0) {
		t.Error("Expect some string features")
	}
	// In Go, range produces a slice, not a new type, but we'll check type
	val := []int{0, 1, 2}
	if typeof(val) != "[]int" {
		t.Errorf("Expected []int type, got %v", typeof(val))
	}
}

func TestPublicBytesTypes(t *testing.T) {
	a := []byte("abc")
	if _, ok := interface{}(a).([]byte); !ok {
		t.Error("Expected a to be []byte")
	}
	b := "def"
	if _, ok := interface{}(b).(string); !ok {
		t.Error("Expected b to be string")
	}
}

func TestPublicStringTypesStr(t *testing.T) {
	s := "something"
	if _, ok := interface{}(s).(string); !ok {
		t.Error("s is not a string")
	}
}

// typeof returns a string representation of the type for basic checks.
func typeof(v interface{}) string {
	return reflect.TypeOf(v).String()
}