package original

import (
	"sort"
	"testing"
)

// Dummy Node and Edge
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
	// For each pair, add edge, accumulate weights
	last := stack[0]
	cg.Nodes[last.ID] = last
	for i := 1; i < len(stack); i++ {
		this := stack[i]
		cg.Nodes[this.ID] = this
		key := [2]int{last.ID, this.ID}
		if cg.Edges[key] == nil {
			cg.Edges[key] = &Edge{Parent: last, Child: this, Weights: map[string]int{}}
		}
		for k, v := range weights {
			cg.Edges[key].Weights[k] += v
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
	// Sort edges by attribute descending
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
	for _, nd := range cg.Nodes {
		nodes = append(nodes, nd)
	}
	sort.Slice(nodes, func(i, j int) bool {
		return nodes[i].Weights[attr] > nodes[j].Weights[attr]
	})
	if n > len(nodes) {
		n = len(nodes)
	}
	return nodes[:n]
}

func TestSimpleCallgraph_BasicAttrs(t *testing.T) {
	graph := NewCallGraph()
	graph.AddStack([]*Node{NewNode(1), NewNode(2)}, map[string]int{"time": 1})
	graph.AddStack([]*Node{NewNode(1), NewNode(3)}, map[string]int{"time": 3})
	graph.AddStack([]*Node{NewNode(1), NewNode(2), NewNode(3)}, map[string]int{"time": 7})
	graph.AddStack([]*Node{NewNode(1), NewNode(4), NewNode(2), NewNode(3)}, map[string]int{"time": 2})

	if len(graph.Nodes) != 4 {
		t.Errorf("Expected 4 nodes, got %d", len(graph.Nodes))
	}
	if len(graph.Edges) != 5 {
		t.Errorf("Expected 5 edges, got %d", len(graph.Edges))
	}
}

func TestSimpleCallgraph_TopEdges(t *testing.T) {
	graph := NewCallGraph()
	graph.AddStack([]*Node{NewNode(1), NewNode(2)}, map[string]int{"time": 1})
	graph.AddStack([]*Node{NewNode(1), NewNode(3)}, map[string]int{"time": 3})
	graph.AddStack([]*Node{NewNode(1), NewNode(2), NewNode(3)}, map[string]int{"time": 7})
	graph.AddStack([]*Node{NewNode(1), NewNode(4), NewNode(2), NewNode(3)}, map[string]int{"time": 2})
	topEdges := graph.GetTopEdges("time", 3)
	var summary [][3]int
	for _, e := range topEdges {
		summary = append(summary, [3]int{e.Parent.ID, e.Child.ID, e.Weights["time"]})
	}
	expected := [][3]int{
		{2, 3, 9},
		{1, 2, 8},
		{1, 3, 3},
	}
	for i := range expected {
		if summary[i] != expected[i] {
			t.Errorf("Edge summary mismatch at %d: got %+v, want %+v", i, summary[i], expected[i])
		}
	}
}

func TestSimpleCallgraph_TopNodes(t *testing.T) {
	graph := NewCallGraph()
	graph.AddStack([]*Node{NewNode(1), NewNode(2)}, map[string]int{"time": 1})
	graph.AddStack([]*Node{NewNode(1), NewNode(3)}, map[string]int{"time": 3})
	graph.AddStack([]*Node{NewNode(1), NewNode(2), NewNode(3)}, map[string]int{"time": 7})
	graph.AddStack([]*Node{NewNode(1), NewNode(4), NewNode(2), NewNode(3)}, map[string]int{"time": 2})
	topNodes := graph.GetTopNodes("time", 2)
	var summary [][2]int
	for _, n := range topNodes {
		summary = append(summary, [2]int{n.ID, n.Weights["time"]})
	}
	expected := [][2]int{
		{3, 12},
		{2, 1},
	}
	for i := range expected {
		if summary[i] != expected[i] {
			t.Errorf("Node summary mismatch at %d: got %+v, want %+v", i, summary[i], expected[i])
		}
	}
}