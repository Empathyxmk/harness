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
func (cg *CallGraph[K]) GetCallers(tgt K) map[K]struct{} {
	callers := make(map[K]struct{})
	for src, tgts := range cg.edges {
		if _, ok := tgts[tgt]; ok {
			callers[src] = struct{}{}
		}
	}
	return callers
}

func TestCallGraphBasicCoverage(t *testing.T) {
	cg := NewCallGraph[string]()
	cg.AddEdge("A", "B")
	cg.AddEdge("A", "C")
	cg.AddEdge("B", "D")

	if _, ok := cg.GetCallees("A")["B"]; !ok {
		t.Error("A should have B as callee")
	}
	if _, ok := cg.GetCallees("A")["C"]; !ok {
		t.Error("A should have C as callee")
	}
	if len(cg.GetCallees("A")) != 2 {
		t.Error("A should have 2 callees")
	}
	if _, ok := cg.GetCallers("B")["A"]; !ok {
		t.Error("B should have A as caller")
	}
	if _, ok := cg.GetCallees("C")["B"]; ok {
		t.Error("C should not have B as callee")
	}
}