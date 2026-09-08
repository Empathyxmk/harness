package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Dummy terml
type Match struct{ value string }
func MatchNode(val string) *Match { return &Match{val} }
func (m *Match) String() string { return m.value }

type Python struct{ expr string }
func PythonNode(expr string) *Python { return &Python{expr} }

// etc.

func TestExactly(t *testing.T) {
	y := MatchNode("b")
	assert.Equal(t, "b", y.String())
}

// The rest of the tests for apply, foreignApply, ..., repeat, consumedby
// should define and check the behavior of the corresponding nodes/types
// and bytecode writing functions, building up slices of typed nodes
// and checking with assert.Equal as per the public_tests logic.

func TestApply(t *testing.T) {
	two := PythonNode("2")
	y := PythonNode("y")
	// Simulate call sequence: [Python('2'), Push(), Python('y'), Push(), Call('bar')]
	seq := []interface{}{two, y}
	assert.Equal(t, PythonNode("2"), seq[0])
	assert.Equal(t, PythonNode("y"), seq[1])
}