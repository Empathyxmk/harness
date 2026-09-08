package original

import (
	"testing"
	"vasco"
)

type DummyContext struct {
	vasco.Context
	ID int
}

func NewDummyCtx(id int) *vasco.Context {
	return &vasco.Context{Method: "m", ID: id}
}

func TestCallSiteEqualsAndHashCode(t *testing.T) {
	ctx1 := NewDummyCtx(1)
	ctx2 := NewDummyCtx(2)
	cs1 := vasco.NewCallSite(ctx1, "call1")
	cs2 := vasco.NewCallSite(ctx1, "call1")
	cs3 := vasco.NewCallSite(ctx1, "call2")
	cs4 := vasco.NewCallSite(ctx2, "call1")

	if !cs1.Equal(cs2) {
		t.Error("Should be equal")
	}
	if cs1.Hash() != cs2.Hash() {
		t.Error("Hashes should match")
	}
	if cs1.Equal(cs3) {
		t.Error("cs1 != cs3")
	}
	if cs1.Equal(cs4) {
		t.Error("cs1 != cs4")
	}
}

func TestCallSiteCompareTo(t *testing.T) {
	ctx1 := NewDummyCtx(1)
	ctx2 := NewDummyCtx(4)
	cs1 := vasco.NewCallSite(ctx1, "c1")
	cs2 := vasco.NewCallSite(ctx2, "c1")

	if cs1.CompareTo(cs2) >= 0 {
		t.Error("cs1 should be less than cs2")
	}
	if cs2.CompareTo(cs1) <= 0 {
		t.Error("cs2 should be greater than cs1")
	}
	if cs1.CompareTo(vasco.NewCallSite(ctx1, "c2")) != 0 {
		t.Error("CompareTo for same ctx id should be zero")
	}
}

func TestCallSiteGettersToString(t *testing.T) {
	ctx1 := NewDummyCtx(42)
	cs1 := vasco.NewCallSite(ctx1, "stmtNode")
	if cs1.GetCallingContext() != ctx1 {
		t.Error("CallingContext wrong")
	}
	if cs1.GetCallNode() != "stmtNode" {
		t.Error("CallNode wrong")
	}
	if !contains(cs1.String(), "42") || !contains(cs1.String(), "stmtNode") {
		t.Error("String should contain values")
	}
}

func contains(str, needle string) bool {
	return len(str) >= len(needle) && str[:len(needle)] == needle || len(needle) == 0
}