package original

import (
	"testing"

	"redisgraph/graph"
	"redisgraph/node"
	"redisgraph/edge"

	"github.com/stretchr/testify/assert"
)

type DummyConnection struct{}

func (DummyConnection) ExecuteCommand(args ...interface{}) interface{} {
	return "EXECUTED"
}

func setupGraph() *graph.Graph {
	return graph.NewGraph("G", DummyConnection{})
}

func TestGraphAddNode(t *testing.T) {
	g := setupGraph()
	n := node.NewNodeWithLabelProperties("Person", map[string]interface{}{"name": "Alice"})
	g.AddNode(n)
	assert.Contains(t, g.Nodes, n)
}

func TestGraphAddEdge(t *testing.T) {
	g := setupGraph()
	n1 := node.NewNodeWithLabelProperties("Person", map[string]interface{}{"name": "Alice"})
	n2 := node.NewNodeWithLabelProperties("Person", map[string]interface{}{"name": "Bob"})
	g.AddNode(n1)
	g.AddNode(n2)
	e := edge.NewEdge(n1, "knows", n2)
	g.AddEdge(e)
	assert.Contains(t, g.Edges, e)
}

func TestGraphCommit(t *testing.T) {
	g := setupGraph()
	n1 := node.NewNodeWithLabelProperties("Person", map[string]interface{}{"name": "Alice"})
	n2 := node.NewNodeWithLabelProperties("Person", map[string]interface{}{"name": "Bob"})
	g.AddNode(n1)
	g.AddNode(n2)
	e := edge.NewEdge(n1, "knows", n2)
	g.AddEdge(e)
	assert.Equal(t, "EXECUTED", g.Commit())
}

func TestGraphDelete(t *testing.T) {
	g := setupGraph()
	assert.Equal(t, "EXECUTED", g.Delete())
}

func TestGraphQuery(t *testing.T) {
	g := setupGraph()
	assert.Equal(t, "EXECUTED", g.Query("MATCH (n) RETURN n"))
}