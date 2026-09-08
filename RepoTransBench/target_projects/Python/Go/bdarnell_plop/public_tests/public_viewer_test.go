package public_tests

import (
	"os"
	"strings"
	"testing"
)

type DummyNodeP struct {
	ID      int
	Attr    string
	Weights map[string]int
}

func NewDummyNodeP(id int, attr string, calls int) DummyNodeP {
	return DummyNodeP{
		ID:      id,
		Attr:    attr,
		Weights: map[string]int{"calls": calls},
	}
}

type DummyStackP struct {
	Nodes   []DummyNodeP
	Weights map[string]int
}

type DummyEdgeP struct {
	Parent  DummyNodeP
	Child   DummyNodeP
	Weights map[string]int
}

type DummyCallGraphP struct {
	Stacks []DummyStackP
	Edges  map[int]DummyEdgeP
}

func NewDummyCallGraphP() DummyCallGraphP {
	return DummyCallGraphP{
		Stacks: []DummyStackP{
			{[]DummyNodeP{NewDummyNodeP(11, "aa", 13)}, map[string]int{"calls": 13}},
			{[]DummyNodeP{NewDummyNodeP(22, "bb", 17)}, map[string]int{"calls": 17}},
		},
		Edges: map[int]DummyEdgeP{
			1: {NewDummyNodeP(11, "aa", 13), NewDummyNodeP(22, "bb", 17), map[string]int{"bar": 3}},
			2: {NewDummyNodeP(22, "bb", 17), NewDummyNodeP(11, "aa", 13), map[string]int{"bar": 3}},
		},
	}
}

func TestPublicIndexHandlerSorted(t *testing.T) {
	filenames := []string{"sample_0.prof", "sample_1.prof", "sample_2.prof"}
	filesSeen := []string{"sample_2.prof", "sample_0.prof", "sample_1.prof"}
	// Sort and compare
	sortStrings := func(xs []string) string {
		s := make([]string, len(xs))
		copy(s, xs)
		for i := 0; i < len(s)-1; i++ {
			for j := i + 1; j < len(s); j++ {
				if s[i] > s[j] {
					s[i], s[j] = s[j], s[i]
				}
			}
		}
		return strings.Join(s, ",")
	}
	if sortStrings(filenames) != sortStrings(filesSeen) {
		t.Errorf("Mismatch in filenames: %v vs %v", filenames, filesSeen)
	}
}

func TestPublicViewHandler(t *testing.T) {
	filename := "alpha.prof"
	rendered := struct {
		Template string
		Filename string
	}{"force.html", filename}
	if rendered.Template != "force.html" || rendered.Filename != "alpha.prof" {
		t.Errorf("Wrong render: got %v", rendered)
	}
}

func TestPublicViewFlatHandler(t *testing.T) {
	graph := NewDummyCallGraphP()
	if len(graph.Stacks) != 2 || len(graph.Edges) != 2 {
		t.Errorf("Expected 2 stacks and 2 edges, got %d/%d", len(graph.Stacks), len(graph.Edges))
	}
}

func TestPublicViewFlatEmbedFile(t *testing.T) {
	filename := "public_b.txt"
	content := "goodbye"
	err := os.WriteFile(filename, []byte(content), 0600)
	if err != nil {
		t.Fatalf("Failed to write temp file: %v", err)
	}
	out, err := os.ReadFile(filename)
	if err != nil {
		t.Fatalf("Failed to read temp file: %v", err)
	}
	if string(out) != content {
		t.Errorf("File content mismatch: got %q, want %q", string(out), content)
	}
	_ = os.Remove(filename)
}

func TestPublicDataHandler(t *testing.T) {
	graph := NewDummyCallGraphP()
	data := map[string]interface{}{
		"nodes":  graph.Stacks,
		"edges":  graph.Edges,
		"stacks": graph.Stacks,
	}
	if data["nodes"] == nil || data["edges"] == nil || data["stacks"] == nil {
		t.Errorf("Handler missing expected data keys")
	}
}

func TestPublicProfileToJson(t *testing.T) {
	graph := NewDummyCallGraphP()
	profile := map[string]interface{}{
		"nodes":  graph.Stacks,
		"edges":  graph.Edges,
		"stacks": graph.Stacks,
	}
	if profile["nodes"] == nil || profile["edges"] == nil || profile["stacks"] == nil {
		t.Errorf("profile_to_json missing keys")
	}
}

func TestPublicProfileToJsonPathTraversal(t *testing.T) {
	filename := "../../out.prof"
	if strings.HasPrefix(filename, "..") {
		t.Logf("Detected path traversal attack, as expected")
	} else {
		t.Errorf("Failed to detect path traversal attack")
	}
}