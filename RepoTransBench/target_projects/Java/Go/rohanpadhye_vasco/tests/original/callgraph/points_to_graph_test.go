package callgraph

import (
	"testing"
)

type PointsToGraph[K comparable, V comparable] struct {
	data map[K]map[V]struct{}
}

func NewPointsToGraph[K comparable, V comparable]() *PointsToGraph[K, V] {
	return &PointsToGraph[K, V]{data: make(map[K]map[V]struct{})}
}

func (p *PointsToGraph[K, V]) Add(k K, v V) {
	if p.data[k] == nil {
		p.data[k] = make(map[V]struct{})
	}
	p.data[k][v] = struct{}{}
}

func (p *PointsToGraph[K, V]) Get(k K) map[V]struct{} {
	return p.data[k]
}

func (p *PointsToGraph[K, V]) Merge(other *PointsToGraph[K, V]) {
	for k, vs := range other.data {
		if p.data[k] == nil {
			p.data[k] = make(map[V]struct{})
		}
		for v := range vs {
			p.data[k][v] = struct{}{}
		}
	}
}

func TestPointsToGraphBasicUsage(t *testing.T) {
	ptg := NewPointsToGraph[string, string]()
	ptg.Add("a", "x")
	ptg.Add("a", "y")
	ptg.Add("b", "z")

	if _, ok := ptg.Get("a")["x"]; !ok {
		t.Error("missing x")
	}
	if _, ok := ptg.Get("a")["y"]; !ok {
		t.Error("missing y")
	}
	if _, ok := ptg.Get("b")["z"]; !ok {
		t.Error("missing z")
	}
	if _, ok := ptg.Get("a")["z"]; ok {
		t.Error("should not have z in a")
	}
}

func TestPointsToGraphMerge(t *testing.T) {
	g1 := NewPointsToGraph[string, string]()
	g2 := NewPointsToGraph[string, string]()
	g1.Add("A", "one")
	g2.Add("A", "two")
	g1.Merge(g2)
	if _, ok := g1.Get("A")["one"]; !ok {
		t.Error("merge failed for one")
	}
	if _, ok := g1.Get("A")["two"]; !ok {
		t.Error("merge failed for two")
	}
}