package tests

import (
	"path/filepath"
	"reflect"
	"testing"
)

// GenerateTestPath returns the full path for test file - mimic Python's os.path.join(__file__, "test-data", path)
func GenerateTestPath(path string) string {
	return filepath.Join("tests", "test-data", path)
}

// AssertEqual provides an assertion equivalent to Python's assert_equal
func AssertEqual(t *testing.T, expected, actual interface{}) {
	if !reflect.DeepEqual(expected, actual) {
		t.Errorf("Not equal:\nexpected: %#v\nactual  : %#v", expected, actual)
	}
}

// AssertRaises runs a function and expects a panic of the given error type
func AssertRaises(t *testing.T, fn func(), expectedType any) error {
	defer func() {
		r := recover()
		if r == nil && expectedType != nil {
			t.Errorf("Did not panic as expected")
		}
		if r != nil && expectedType != nil {
			if reflect.TypeOf(r) != reflect.TypeOf(expectedType) {
				t.Errorf("Panicked with wrong type. Got %T, expected %T", r, expectedType)
			}
		}
	}()
	fn()
	return nil
}