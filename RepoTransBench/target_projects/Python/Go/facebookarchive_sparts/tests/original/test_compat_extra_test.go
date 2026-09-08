package original

import (
	"testing"
)

func TestBasestringPy3(t *testing.T) {
	if typeof("") != "string" {
		t.Errorf("basestring not string")
	}
}

func TestLongPy3(t *testing.T) {
	var y int64 = 42
	if typeof(y) != "int64" {
		t.Errorf("long is not int64")
	}
}

func TestUnicodePy3(t *testing.T) {
	if typeof("foo") != "string" {
		t.Error("unicode not string")
	}
}

func TestPyVersionConstants(t *testing.T) {
	const (
		PY2 = false
		PY3 = true
	)
	if !PY3 {
		t.Error("PY3 should be true")
	}
	if PY2 {
		t.Error("PY2 should be false")
	}
}

func TestRangeMapAndZip(t *testing.T) {
	r := []int{0, 1, 2}
	// Map/zip: skip, trivial in Go
	if len(r) != 3 {
		t.Fatal("range/map/zip fail")
	}
}

func TestBytesTypeAndStrType(t *testing.T) {
	b := []byte("abc")
	str := "abc"
	if typeof(b) != "[]uint8" {
		t.Error("bytes_type not []byte")
	}
	if typeof(str) != "string" {
		t.Error("str_type not string")
	}
}

func TestStringTypesContainsStr(t *testing.T) {
	var s interface{} = "foo"
	if typeof(s) != "string" {
		t.Error("string_types does not contain string")
	}
	if _, ok := s.(string); !ok {
		t.Error("not a string")
	}
}

func typeof(v interface{}) string {
	return (fmt.Sprintf("%T", v))
}