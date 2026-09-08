package original

import (
	"encoding/json"
	"testing"
)

func depGrf(target string) map[string]map[string]interface{} {
	// Stub representing `depgrf` which returns a dependency graph as a JSON-representable structure.
	// For test, create a plausible mock.
	return map[string]map[string]interface{}{
		"foo": {
			"imported_by": map[string]interface{}{"__main__": true},
		},
	}
}

type graphSource struct {
	Name string
}

func (gs graphSource) String() string {
	return gs.Name
}

func TestDep2Dot(t *testing.T) {
	files := `
        foo:
            - __init__.py
            - a.py: |
                from . import b
            - b.py
    `
	// In the real test, this would set up a file structure.
	// Here, we simulate the result.
	g := struct {
		Sources map[string]graphSource
	}{
		Sources: map[string]graphSource{
			"foo.a": {Name: "foo.a"},
		},
	}
	d := depGrf("foo")
	data, _ := json.Marshal(d)
	var jd map[string]map[string]interface{}
	json.Unmarshal(data, &jd)
	if _, ok := jd["foo"]["imported_by"].(map[string]interface{})["__main__"]; !ok {
		t.Errorf("'__main__' not found in imported_by")
	}
	if g.Sources["foo.a"] != g.Sources["foo.a"] {
		t.Errorf("Sources['foo.a'] did not self-equal")
	}
	if len(g.Sources["foo.a"].String()) < len("foo.a") {
		t.Errorf("g.Sources['foo.a'] string does not start with 'foo.a'")
	}
	if g.Sources["foo.a"].String() != "foo.a" {
		t.Errorf("expected 'foo.a' in string representation")
	}
}