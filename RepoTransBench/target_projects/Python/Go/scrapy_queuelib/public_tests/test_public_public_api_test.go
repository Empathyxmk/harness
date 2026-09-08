package public_tests

import (
	"testing"
)

var queuelib = map[string]interface{}{
	"__version__": "1.0.0",
	"pqueue": map[string]interface{}{"PriorityQueue": true},
	"rrqueue": map[string]interface{}{"RoundRobinQueue": true},
}

func TestPublicApiPublic(t *testing.T) {
	// Simulate: hasattr(queuelib, "__version__") or hasattr(queuelib, "version")
	version, ok := queuelib["__version__"]
	if !ok {
		if _, ok2 := queuelib["version"]; !ok2 {
			t.Error("queuelib should have __version__ or version attribute")
		} else {
			version = queuelib["version"]
		}
	}
	// Check version looks like "A.B"
	if s, ok := version.(string); ok {
		if len(s) < 3 || s[1] != '.' {
			t.Errorf("version string %q does not look like 'A.B'", s)
		}
	}
	// Check pqueue and rrqueue keys and that they contain classes.
	if _, ok := queuelib["pqueue"]; !ok {
		t.Error("queuelib should have attribute pqueue")
	}
	if _, ok := queuelib["rrqueue"]; !ok {
		t.Error("queuelib should have attribute rrqueue")
	}
	pq := queuelib["pqueue"].(map[string]interface{})
	rq := queuelib["rrqueue"].(map[string]interface{})
	if _, ok := pq["PriorityQueue"]; !ok {
		t.Error("queuelib.pqueue must have PriorityQueue class")
	}
	if _, ok := rq["RoundRobinQueue"]; !ok {
		t.Error("queuelib.rrqueue must have RoundRobinQueue class")
	}
}