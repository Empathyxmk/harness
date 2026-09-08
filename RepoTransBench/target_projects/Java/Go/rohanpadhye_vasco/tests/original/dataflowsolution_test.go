package original

import (
	"testing"
	"vasco"
)

func TestSetAndGet(t *testing.T) {
	dfs := vasco.NewDataFlowSolution[string, int]()
	dfs.Set("A", []int{42})
	g := dfs.Get("A")
	if len(g) == 0 || g[0] != 42 {
		t.Error("expected to contain 42")
	}
	keys := dfs.KeySet()
	if len(keys) == 0 || keys[0] != "A" {
		t.Error("keyset should contain A")
	}
}

func TestMerge(t *testing.T) {
	dfs1 := vasco.NewDataFlowSolution[string, int]()
	dfs2 := vasco.NewDataFlowSolution[string, int]()
	dfs1.Set("A", []int{1})
	dfs2.Set("A", []int{2})
	dfs1.Merge(dfs2)
	content := dfs1.Get("A")
	has1 := false
	has2 := false
	for _, n := range content {
		if n == 1 {
			has1 = true
		}
		if n == 2 {
			has2 = true
		}
	}
	if !has1 || !has2 {
		t.Error("merge failed")
	}
}

func TestToString(t *testing.T) {
	dfs := vasco.NewDataFlowSolution[string, int]()
	dfs.Set("B", []int{100})
	str := dfs.String()
	if str != "DataFlowSolution" {
		t.Error("unexpected string content")
	}
}