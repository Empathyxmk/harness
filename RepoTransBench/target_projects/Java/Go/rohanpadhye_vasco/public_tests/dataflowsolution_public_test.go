package public_tests

import (
	"testing"
	"vasco"
)

func TestDifferentInOutValues(t *testing.T) {
	in := map[string]int{"A": 111, "B": 222}
	out := map[string]int{"A": 777, "B": 888}
	dfs := vasco.NewDataFlowSolutionInOut[string, int](in, out)

	if dfs.GetValueBefore("A") != 111 {
		t.Error("value before A")
	}
	if dfs.GetValueBefore("B") != 222 {
		t.Error("value before B")
	}
	if dfs.GetValueAfter("A") != 777 {
		t.Error("after A")
	}
	if dfs.GetValueAfter("B") != 888 {
		t.Error("after B")
	}
}

func TestNullReturnFromMaps(t *testing.T) {
	in := map[string]int{}
	out := map[string]int{}
	dfs := vasco.NewDataFlowSolutionInOut[string, int](in, out)

	if dfs.GetValueBefore("notPresent") != 0 {
		t.Error("Should return zero value for missing")
	}
	if dfs.GetValueAfter("notPresent") != 0 {
		t.Error("Should return zero value for missing")
	}
}