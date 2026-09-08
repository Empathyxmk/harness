package callgraph

import (
	"testing"
)

type CallGraph[K comparable] struct {
	edges map[K]map[K]struct{}
}
func NewCallGraph[K comparable]() *CallGraph[K] {
	return &CallGraph[K]{edges: make(map[K]map[K]struct{})}
}
func (cg *CallGraph[K]) AddEdge(src, tgt K) {
	if cg.edges[src] == nil {
		cg.edges[src] = make(map[K]struct{})
	}
	cg.edges[src][tgt] = struct{}{}
}
func (cg *CallGraph[K]) GetCallees(src K) map[K]struct{} {
	return cg.edges[src]
}
type CallGraphTransformer[K comparable] interface {
	Transform(*CallGraph[K])
}
type dummyTransformer struct{}
func (dummyTransformer) Transform(g *CallGraph[string]) {}

func TestCallGraphTransformerCoverage(t *testing.T) {
	cg := NewCallGraph[string]()
	cg.AddEdge("A", "B")
	t := dummyTransformer{}
	t.Transform(cg)
	cg.AddEdge("B", "C")
	if _, ok := cg.GetCallees("B")["C"]; !ok {
		t.Error("expected B->C")
	}
}