package public_tests

import (
	"testing"
	"errors"

	"github.com/stretchr/testify/assert"
)

// Minimal Graph and Operation implementations for public tests
type DummyOp struct {
	Name  string
	Graph *Graph
}

type Graph struct {
	operations map[string]*DummyOp
}

func NewGraph() *Graph {
	return &Graph{operations: map[string]*DummyOp{}}
}

func (g *Graph) AddOperation(op *DummyOp) {
	g.operations[op.Name] = op
}

func (g *Graph) NormalizeOperation(arg interface{}) *DummyOp {
	switch x := arg.(type) {
	case *DummyOp:
		return x
	case string:
		if op, ok := g.operations[x]; ok {
			return op
		}
		panic(errors.New("not found"))
	default:
		panic(errors.New("invalid normalization"))
	}
}

func NewDummyOp(name string, g *Graph) *DummyOp {
	return &DummyOp{Name: name, Graph: g}
}

func TestGraphAddOperation(t *testing.T) {
	g := NewGraph()
	op := NewDummyOp("foo", g)
	g.AddOperation(op)
	assert.Equal(t, op, g.NormalizeOperation("foo"))
	assert.Equal(t, op, g.NormalizeOperation(op))
}

func TestGraphNormalizeOperationInvalid(t *testing.T) {
	g := NewGraph()
	assert.Panics(t, func() {
		g.NormalizeOperation(3)
	})
	assert.Panics(t, func() {
		g.NormalizeOperation("notfound")
	})
}