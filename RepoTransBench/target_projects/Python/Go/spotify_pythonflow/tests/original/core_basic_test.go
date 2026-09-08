package original

import (
	"testing"
	"errors"

	"github.com/stretchr/testify/assert"
)

// You will need to implement the Graph and Operation interfaces in your Go version.
type DummyOp struct {
	Name  string
	Graph *Graph
}

func (op *DummyOp) Evaluate() interface{} {
	// Dummy evaluate returns 42 for testing
	return 42
}

func TestGraphEnterExit(t *testing.T) {
	g := NewGraph()
	assert.Nil(t, g.defaultGraph)
	g.Enter()
	assert.Equal(t, g, defaultGraph)
	g.Exit()
	assert.Nil(t, g.defaultGraph)
}

func TestGraphDuplicateEnter(t *testing.T) {
	g := NewGraph()
	g.Enter()
	defer g.Exit()
	assert.Panics(t, func() {
		g.Enter()
	})
}

func TestGraphNormalizeOperationWithInstance(t *testing.T) {
	g := NewGraph()
	op := NewDummyOp("abc", g)
	g.operations["abc"] = op
	assert.Equal(t, g.NormalizeOperation(op), op)

	other := NewGraph()
	op2 := NewDummyOp("def", other)
	err := func() (err error) {
		defer func() {
			if r := recover(); r != nil {
				if e, ok := r.(error); ok {
					err = e
				} else {
					err = errors.New("unexpected error")
				}
			}
		}()
		g.NormalizeOperation(op2)
		return nil
	}()
	assert.NotNil(t, err)
}

func TestGraphNormalizeOperationWithName(t *testing.T) {
	g := NewGraph()
	op := NewDummyOp("abc", g)
	g.operations["abc"] = op
	assert.Equal(t, g.NormalizeOperation("abc"), op)
}

func TestGraphNormalizeOperationInvalid(t *testing.T) {
	g := NewGraph()
	assert.Panics(t, func() {
		g.NormalizeOperation(123)
	})
	assert.Panics(t, func() {
		g.NormalizeOperation("notfound")
	})
}

func TestGraphNormalizeContextAndDuplicates(t *testing.T) {
	g := NewGraph()
	op := NewDummyOp("x", g)
	g.operations["x"] = op
	ctx := map[string]interface{}{"x": 3}
	norm := g.NormalizeContext(ctx)
	assert.Contains(t, norm, op)

	assert.Panics(t, func() {
		g.NormalizeContext([2]interface{}{"x", 3})
	})

	ctxDup := map[interface{}]interface{}{op: 1, "x": 2}
	assert.Panics(t, func() {
		g.NormalizeContext(ctxDup)
	})
}

func TestGraphNormalizeContextKwargs(t *testing.T) {
	g := NewGraph()
	op := NewDummyOp("x", g)
	g.operations["x"] = op
	norm := g.NormalizeContextWithKwargs(nil, map[string]interface{}{"x": 99})
	assert.Contains(t, norm, op)
	assert.Equal(t, norm[op], 99)
}

// Mock structures/constructors for this test file. Your core implementation must provide real ones.
type Graph struct {
	defaultGraph *Graph
	operations   map[string]*DummyOp
}

var defaultGraph *Graph

func NewGraph() *Graph {
	return &Graph{operations: map[string]*DummyOp{}}
}
func (g *Graph) Enter()      { defaultGraph = g; g.defaultGraph = g }
func (g *Graph) Exit()       { defaultGraph = nil; g.defaultGraph = nil }
func (g *Graph) NormalizeOperation(arg interface{}) *DummyOp {
	switch x := arg.(type) {
	case *DummyOp:
		if x.Graph == g {
			return x
		}
		panic(errors.New("operation belongs to other graph"))
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
func (g *Graph) NormalizeContext(ctx interface{}) map[*DummyOp]interface{} {
	switch c := ctx.(type) {
	case map[string]interface{}:
		out := make(map[*DummyOp]interface{})
		for k, v := range c {
			if op, ok := g.operations[k]; ok {
				if _, exists := out[op]; exists {
					panic(errors.New("duplicate key"))
				}
				out[op] = v
			} else {
				panic(errors.New("bad key"))
			}
		}
		return out
	case map[interface{}]interface{}:
		seen := map[*DummyOp]struct{}{}
		for key := range c {
			switch k := key.(type) {
			case *DummyOp:
				if _, ok := seen[k]; ok {
					panic(errors.New("duplicate key"))
				}
				seen[k] = struct{}{}
			case string:
				if op, ok := g.operations[k]; ok {
					if _, ok := seen[op]; ok {
						panic(errors.New("duplicate key"))
					}
					seen[op] = struct{}{}
				}
			}
		}
		panic(errors.New("context not a mapping"))
	default:
		panic(errors.New("context not a mapping"))
	}
}
func (g *Graph) NormalizeContextWithKwargs(ctx map[string]interface{}, kwargs map[string]interface{}) map[*DummyOp]interface{} {
	if ctx == nil {
		ctx = map[string]interface{}{}
	}
	for k, v := range kwargs {
		ctx[k] = v
	}
	return g.NormalizeContext(ctx)
}