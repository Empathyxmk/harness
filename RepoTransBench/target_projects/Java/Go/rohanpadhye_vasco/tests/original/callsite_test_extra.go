package original

import (
	"strings"
	"testing"
	"vasco"
)

func TestCallSiteEqualsAndHashCodeExtra(t *testing.T) {
	cs1 := vasco.NewCallSite(&vasco.Context{Method: "foo", ID: 1}, "foo")
	cs2 := vasco.NewCallSite(&vasco.Context{Method: "foo", ID: 1}, "foo")
	cs3 := vasco.NewCallSite(&vasco.Context{Method: "bar", ID: 2}, "bar")

	if !cs1.Equal(cs2) {
		t.Error("cs1 should equal cs2")
	}
	if cs1.Equal(cs3) {
		t.Error("cs1 should not equal cs3")
	}
	if cs1.Hash() != cs2.Hash() {
		t.Error("hash codes should match")
	}
	if cs1.Hash() == cs3.Hash() {
		t.Error("hash codes should NOT match")
	}
}

func TestCallSiteToStringExtra(t *testing.T) {
	cs := vasco.NewCallSite(&vasco.Context{Method: "main", ID: 3}, "main")
	str := cs.String()
	if !strings.Contains(str, "main") || !strings.Contains(str, "3") {
		t.Error("toString must contain method and id")
	}
}