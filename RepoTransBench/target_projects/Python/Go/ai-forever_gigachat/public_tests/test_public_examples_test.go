package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type SimpleExample struct {
	Q string
	A string
}
func (s SimpleExample) String() string    { return "Q: " + s.Q + "\nA: " + s.A }
func (s SimpleExample) GoString() string  { return "SimpleExample(" + s.Q + ", " + s.A + ")" }

type SimpleFunctionExample struct {
	Fn     string
	Params map[string]interface{}
	Out    string
}
func (s SimpleFunctionExample) String() string   { return "Function: " + s.Fn }
func (s SimpleFunctionExample) GoString() string { return "SimpleFunctionExample(" + s.Fn + ")" }

func TestSimpleExampleReprAndStr(t *testing.T) {
	se := SimpleExample{"Who created the Eiffel Tower?", "Gustave Eiffel built it in Paris."}
	assert.Contains(t, se.Q, "Who created")
	assert.Contains(t, se.A, "Paris.")
	assert.Contains(t, se.GoString(), "Eiffel")
}

func TestSimpleFunctionExampleReprAndStr(t *testing.T) {
	sfe := SimpleFunctionExample{"weather", map[string]interface{}{"city": "Tokyo", "year": 2022}, "performed"}
	assert.Equal(t, "weather", sfe.Fn)
	assert.Equal(t, "Tokyo", sfe.Params["city"])
	assert.Equal(t, "performed", sfe.Out)
}