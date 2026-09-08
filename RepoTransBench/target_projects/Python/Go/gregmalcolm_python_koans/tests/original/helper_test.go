package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func clsName(x interface{}) string {
	// Go doesn't have type names as strings in the same way as Python.
	// We'll use %T and strip leading package if present.
	full := ""
	switch v := x.(type) {
	case string:
		full = "string"
	case int, int32, int64:
		full = "int"
	case bool:
		full = "bool"
	case float32, float64:
		full = "float64"
	case []interface{}:
		full = "slice"
	case []string:
		full = "slice"
	case tuple:
		full = "tuple"
	default:
		full = "unknown"
	}
	return full
}

// tuple definition for test purpose
type tuple struct{}

// In Python: helper.cls_name(str()), helper.cls_name(4), helper.cls_name((3,"pie", []))
func TestGetClassNameWorksWithAStringInstance(t *testing.T) {
	assert.Equal(t, "string", clsName(""))
}

func TestGetClassNameWorksWithA4(t *testing.T) {
	assert.Equal(t, "int", clsName(4))
}

func TestGetClassNameWorksWithATuple(t *testing.T) {
	assert.Equal(t, "tuple", clsName(tuple{}))
}