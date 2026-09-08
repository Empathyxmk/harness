package original

import (
	"testing"

	"redisgraph/node"
	"redisgraph/edge"
	"redisgraph/path"

	"github.com/stretchr/testify/assert"
)

func TestPathInit(t *testing.T) {
	assert.Panics(t, func() {
		path.NewPath(nil, nil)
	})

	assert.Panics(t, func() {
		path.NewPath([]*node.Node{}, nil)
	})

	assert.Panics(t, func() {
		path.NewPath(nil, []*edge.Edge{})
	})

	assert.NotNil(t, path.NewPath([]*node.Node{}, []*edge.Edge{}))
}

func TestPathNewEmptyPath(t *testing.T) {
	newEmptyPath := path.NewEmptyPath()
	assert.NotNil(t, newEmptyPath)
	assert.Empty(t, newEmptyPath.Nodes())
	assert.Empty(t, newEmptyPath.Edges())
}

func TestPathWrongFlows(t *testing.T) {
	node1 := node.NewNodeWithID(1)
	node2 := node.NewNodeWithID(2)
	node3 := node.NewNodeWithID(3)

	edge1 := edge.NewEdge(node1, nil, node2)
	edge2 := edge.NewEdge(node1, nil, node3)

	p := path.NewEmptyPath()
	assert.Panics(t, func() {
		p.AddEdge(edge1)
	})

	p.AddNode(node1)
	assert.Panics(t, func() {
		p.AddNode(node2)
	})

	p.AddEdge(edge1)
	assert.Panics(t, func() {
		p.AddEdge(edge2)
	})
}

func TestPathNodesAndEdges(t *testing.T) {
	node1 := node.NewNodeWithID(1)
	node2 := node.NewNodeWithID(2)
	edge1 := edge.NewEdge(node1, nil, node2)

	p := path.NewEmptyPath()
	assert.Equal(t, []*node.Node{}, p.Nodes())
	p.AddNode(node1)
	assert.Equal(t, []*edge.Edge{}, p.Edges())
	assert.Equal(t, 0, p.EdgeCount())
	assert.Equal(t, []*node.Node{node1}, p.Nodes())
	assert.Equal(t, node1, p.GetNode(0))
	assert.Equal(t, node1, p.FirstNode())
	assert.Equal(t, node1, p.LastNode())
	assert.Equal(t, 1, p.NodesCount())
	p.AddEdge(edge1)
	assert.Equal(t, []*edge.Edge{edge1}, p.Edges())
	assert.Equal(t, 1, p.EdgeCount())
	assert.Equal(t, edge1, p.GetRelationship(0))
	p.AddNode(node2)
	assert.Equal(t, []*node.Node{node1, node2}, p.Nodes())
	assert.Equal(t, node1, p.FirstNode())
	assert.Equal(t, node2, p.LastNode())
	assert.Equal(t, 2, p.NodesCount())
}

func TestPathCompare(t *testing.T) {
	node1 := node.NewNodeWithID(1)
	node2 := node.NewNodeWithID(2)
	edge1 := edge.NewEdge(node1, nil, node2)

	assert.Equal(t, path.NewEmptyPath(), path.NewEmptyPath())
	assert.Equal(t, path.NewPath([]*node.Node{node1, node2}, []*edge.Edge{edge1}), path.NewPath([]*node.Node{node1, node2}, []*edge.Edge{edge1}))
	assert.NotEqual(t, path.NewPath([]*node.Node{node1}, []*edge.Edge{}), path.NewPath([]*node.Node{}, []*edge.Edge{}))
	assert.NotEqual(t, path.NewPath([]*node.Node{node1}, []*edge.Edge{}), path.NewPath([]*node.Node{}, []*edge.Edge{}))
	assert.NotEqual(t, path.NewPath([]*node.Node{node1}, []*edge.Edge{}), path.NewPath([]*node.Node{node2}, []*edge.Edge{}))
	assert.NotEqual(t, path.NewPath([]*node.Node{node1}, []*edge.Edge{edge1}), path.NewPath([]*node.Node{node1}, []*edge.Edge{}))
	assert.NotEqual(t, path.NewPath([]*node.Node{node1}, []*edge.Edge{edge1}), path.NewPath([]*node.Node{node2}, []*edge.Edge{edge1}))
}