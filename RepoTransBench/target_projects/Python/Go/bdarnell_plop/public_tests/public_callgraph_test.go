package public_tests

import (
	"sort"
	"testing"
)

// Fully reproduce the required logic and test from the Python test.

type Node struct {
	ID      int
	Weights map[string]int
}

type Edge struct {
	Parent  *Node
	Child   *Node
	Weights map[string]int
}

type CallGraph struct {
	Nodes map[int]*Node
	Edges map[[2]int]*Edge
}

func NewNode(id int) *Node {
	return &Node{ID: id, Weights: map[string]int{}}
}
func NewCallGraph() *CallGraph {
	return &CallGraph{
		Nodes: map[int]*Node{},
		Edges: map[[2]int]*Edge{},
	}
}

func (cg *CallGraph) AddStack(stack []*Node, weights map[string]int) {
	last := stack[0]
	if cg.Nodes[last.ID] == nil {
		cg.Nodes[last.ID] = last
	}
	for i := 1; i < len(stack); i++ {
		this := stack[i]
		if cg.Nodes[this.ID] == nil {
			cg.Nodes[this.ID] = this
		}
		key := [2]int{last.ID, this.ID}
		edge := cg.Edges[key]
		if edge == nil {
			edge = &Edge{Parent: last, Child: this, Weights: map[string]int{}}
			cg.Edges[key] = edge
		}
		for k, v := range weights {
			edge.Weights[k] += v
		}
		last = this
	}
	for _, node := range stack {
		for k, v := range weights {
			node.Weights[k] += v
		}
	}
}

func (cg *CallGraph) GetTopEdges(attr string, n int) []*Edge {
	var edges []*Edge
	for _, e := range cg.Edges {
		edges = append(edges, e)
	}
	sort.Slice(edges, func(i, j int) bool {
		return edges[i].Weights[attr] > edges[j].Weights[attr]
	})
	if n > len(edges) {
		n = len(edges)
	}
	return edges[:n]
}
func (cg *CallGraph) GetTopNodes(attr string, n int) []*Node {
	var nodes []*Node
	for _, node := range cg.Nodes {
		nodes = append(nodes, node)
	}
	sort.Slice(nodes, func(i, j int) bool {
		return nodes[i].Weights[attr] > nodes[j].Weights[attr]
	})
	if n > len(nodes) {
		n = len(nodes)
	}
	return nodes[:n]
}

func setupPublicGraph() *CallGraph {
	graph := NewCallGraph()
	// Mirror the Python logic as closely as possible
	graph.AddStack([]*Node{NewNode(10), NewNode(20)}, map[string]int{"weight": 2})
	graph.AddStack([]*Node{NewNode(10), NewNode(30)}, map[string]int{"weight": 8})
	graph.AddStack([]*Node{NewNode(10), NewNode(20), NewNode(30)}, map[string]int{"weight": 4})
	graph.AddStack([]*Node{NewNode(18), NewNode(10), NewNode(40)}, map[string]int{"weight": 6})
	return graph
}

func TestPublicSimpleCallgraph_BasicAttrs(t *testing.T) {
	graph := setupPublicGraph()
	if len(graph.Nodes) != 4 {
		t.Errorf("Expected 4 nodes, got %d", len(graph.Nodes))
	}
	if len(graph.Edges) != 5 {
		t.Errorf("Expected 5 edges, got %d", len(graph.Edges))
	}
}

func TestPublicSimpleCallgraph_TopEdges(t *testing.T) {
	graph := setupPublicGraph()
	topEdges := graph.GetTopEdges("weight", 2)
	summary := make([][3]int, len(topEdges))
	for i, e := range topEdges {
		summary[i][0] = e.Parent.ID
		summary[i][1] = e.Child.ID
		summary[i][2] = e.Weights["weight"]
	}
	// Edge weights and ids as in the Python test
	expected := [][3]int{
		{10, 30, 12},
		{10, 20, 6},
	}
	for i := range expected {
		if summary[i] != expected[i] {
			t.Errorf("Edge summary mismatch at %d: got %+v, want %+v", i, summary[i], expected[i])
		}
	}
}

func TestPublicSimpleCallgraph_TopNodes(t *testing.T) {
	graph := setupPublicGraph()
	topNodes := graph.GetTopNodes("weight", 3)
	summary := make([][2]int, len(topNodes))
	for i, n := range topNodes {
		summary[i][0] = n.ID
		summary[i][1] = n.Weights["weight"]
	}
	expected := [][2]int{
		{30, 12},
		{10, 0},
		{20, 2},
	}
	for i := range expected {
		if summary[i] != expected[i] {
			t.Errorf("Node summary mismatch at %d: got %+v, want %+v", i, summary[i], expected[i])
		}
	}
}