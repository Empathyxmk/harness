package public_tests

import (
	"encoding/json"
	"testing"
)

func depGrf(target string) map[string]map[string]interface{} {
	return map[string]map[string]interface{}{
		"bar": {
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

func TestDep2DotPublic(t *testing.T) {
	files := `
        bar:
            - __init__.py
            - x.py: |
                from . import y
            - y.py
    `
	g := struct {
		Sources map[string]graphSource
	}{
		Sources: map[string]graphSource{
			"bar.x": {Name: "bar.x"},
		},
	}
	d := depGrf("bar")
	data, _ := json.Marshal(d)
	var jd map[string]map[string]interface{}
	json.Unmarshal(data, &jd)
	if _, ok := jd["bar"]["imported_by"].(map[string]interface{})["__main__"]; !ok {
		t.Errorf("'__main__' not found in imported_by")
	}
	if g.Sources["bar.x"] != g.Sources["bar.x"] {
		t.Errorf("Sources['bar.x'] did not self-equal")
	}
	if len(g.Sources["bar.x"].String()) < len("bar.x") {
		t.Errorf("g.Sources['bar.x'] string does not start with 'bar.x'")
	}
	if g.Sources["bar.x"].String() != "bar.x" {
		t.Errorf("expected 'bar.x' in string representation")
	}
}