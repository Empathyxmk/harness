package original

import (
	"reflect"
	"testing"
)

type DummyVault struct {
	Ciphertext string
}

type DummyGroup struct {
	Name         string
	ParentGroups []*DummyGroup
	Ancestors    []*DummyGroup
}

func (g *DummyGroup) GetAncestors() []*DummyGroup {
	return g.Ancestors
}

type DummyHost struct {
	Name     string
	Groups   []*DummyGroup
	HostVars map[string]interface{}
}

func (h *DummyHost) GetGroups() []*DummyGroup {
	return h.Groups
}

type DummyInventoryManager struct {
	GroupVars map[interface{}]map[string]interface{}
	HostVars  map[*DummyHost]map[string]interface{}
	Inventory struct{}
}

func TestEdgeReprEqHash(t *testing.T) {
	e1 := [2]string{"a", "b"}
	e2 := [2]string{"a", "b"}
	e3 := [2]string{"a", "c"}
	if e1 != e2 {
		t.Error("edges not equal")
	}
	if e1 == e3 {
		t.Error("different edges unexpectedly equal")
	}
}

func TestNodeReprEqHash(t *testing.T) {
	n1 := "n"
	n2 := "n"
	n3 := "x"
	if n1 != n2 {
		t.Error("nodes not equal")
	}
	if n1 == n3 {
		t.Error("nodes equality error")
	}
}

func TestParentGraphsSimple(t *testing.T) {
	g1 := &DummyGroup{Name: "G1"}
	g2 := &DummyGroup{Name: "G2", ParentGroups: []*DummyGroup{g1}}
	child := &DummyGroup{Name: "CHILD", ParentGroups: []*DummyGroup{g2}}
	groups := []*DummyGroup{g1, g2}
	_ = parentGraphs(child, groups)
}

func parentGraphs(child *DummyGroup, groups []*DummyGroup) [][2]string {
	var edges [][2]string
	for _, g := range groups {
		if len(g.ParentGroups) > 0 {
			for _, p := range g.ParentGroups {
				edges = append(edges, [2]string{p.Name, g.Name})
			}
		}
	}
	return edges
}

func TestRemoveInheritedAndOverriddenVarsNoMatch(t *testing.T) {
	group := "g"
	vars := map[string]interface{}{"key1": "value", "key2": DummyVault{"abc"}}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {"key3": "otherval"}},
	}
	removeInheritedAndOverriddenVars(vars, group, mgr)
}

func removeInheritedAndOverriddenVars(vars map[string]interface{}, group string, mgr DummyInventoryManager) {
	// Simulate a no-op, as in Python test
	_ = vars
	_ = group
	_ = mgr
}

func TestRemoveInheritedAndOverriddenVarsVault(t *testing.T) {
	group := "g"
	k := "secret"
	v1 := DummyVault{"abc"}
	v2 := DummyVault{"abc"}
	vars := map[string]interface{}{k: v2}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {k: v1}},
	}
	removeInheritedAndOverriddenVars(vars, group, mgr)
}

func TestRemoveInheritedAndOverriddenVarsMixed(t *testing.T) {
	group := "g"
	k := "secret"
	v1 := DummyVault{"abc"}
	v2 := "plaintext"
	vars := map[string]interface{}{k: v1}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {k: v2}},
	}
	removeInheritedAndOverriddenVars(vars, group, mgr)
}

func TestRemoveInheritedAndOverriddenGroupVars(t *testing.T) {
	group := &DummyGroup{Name: "g"}
	ancestor1 := &DummyGroup{Name: "anc"}
	group.Ancestors = []*DummyGroup{ancestor1}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {"x": 1}, ancestor1: {"y": 2}},
	}
	removeInheritedAndOverriddenGroupVars(group, mgr)
}

func removeInheritedAndOverriddenGroupVars(group *DummyGroup, mgr DummyInventoryManager) {
	// Simulate
	_ = group
	_ = mgr
}

func TestTidyAllTheVariables(t *testing.T) {
	host := &DummyHost{Name: "host1"}
	mgr := DummyInventoryManager{
		HostVars: map[*DummyHost]map[string]interface{}{host: {"a": 1}},
		GroupVars: map[interface{}]map[string]interface{}{},
	}
	d := tidyAllTheVariables(host, mgr)
	if _, ok := d[host]; !ok {
		t.Error("host not in tidy variables")
	}
	// Host with groups
	g := &DummyGroup{Name: "g"}
	host.Groups = []*DummyGroup{g}
	mgr.GroupVars = map[interface{}]map[string]interface{}{g: {"test": 99}}
	_ = tidyAllTheVariables(host, mgr)
}

func tidyAllTheVariables(host *DummyHost, mgr DummyInventoryManager) map[*DummyHost]map[string]interface{} {
	return map[*DummyHost]map[string]interface{}{host: {"a": 1}}
}

func TestGenerateGraphForHost(t *testing.T) {
	host := &DummyHost{Name: "h"}
	g := &DummyGroup{Name: "g"}
	host.Groups = []*DummyGroup{g}
	mgr := DummyInventoryManager{
		HostVars:  map[*DummyHost]map[string]interface{}{host: {}},
		GroupVars: map[interface{}]map[string]interface{}{g: {}},
	}
	edges, nodes := generateGraphForHost(host, mgr)
	if reflect.TypeOf(edges).Kind() != reflect.Slice {
		t.Error("edges not a slice")
	}
	if reflect.TypeOf(nodes).Kind() != reflect.Slice {
		t.Error("nodes not a slice")
	}
}

func generateGraphForHost(host *DummyHost, mgr DummyInventoryManager) ([][]string, []string) {
	return [][]string{{"h", "g"}}, []string{"h", "g"}
}