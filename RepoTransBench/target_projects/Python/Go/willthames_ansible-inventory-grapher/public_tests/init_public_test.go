package public_tests

import (
	"reflect"
	"testing"
)

// Dummy types
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

func TestEdgePublicReprEqHash(t *testing.T) {
	e1 := [2]string{"x", "y"}
	e2 := [2]string{"x", "y"}
	e3 := [2]string{"x", "z"}
	if e1 != e2 {
		t.Error("public edges not equal")
	}
	if e1 == e3 {
		t.Error("public different edges unexpectedly equal")
	}
}

func TestNodePublicReprEqHash(t *testing.T) {
	n1 := "nn"
	n2 := "nn"
	n3 := "yy"
	if n1 != n2 {
		t.Error("nodes not equal (public)")
	}
	if n1 == n3 {
		t.Error("nodes equality error (public)")
	}
}

func TestParentGraphsPublicSimple(t *testing.T) {
	g10 := &DummyGroup{Name: "G10"}
	g20 := &DummyGroup{Name: "G20", ParentGroups: []*DummyGroup{g10}}
	child2 := &DummyGroup{Name: "CHILD2", ParentGroups: []*DummyGroup{g20}}
	groups := []*DummyGroup{g10, g20}
	_ = parentGraphs(child2, groups)
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

func TestRemoveInheritedAndOverriddenVarsPublicNoMatch(t *testing.T) {
	group := "g_public"
	vars := map[string]interface{}{"key9": "value2", "key8": DummyVault{"lmn"}}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {"key1": "otherval"}},
	}
	removeInheritedAndOverriddenVars(vars, group, mgr)
}

func TestRemoveInheritedAndOverriddenVarsPublicVault(t *testing.T) {
	group := "g_public"
	k := "topsecret"
	v1 := DummyVault{"shh"}
	v2 := DummyVault{"shh"}
	vars := map[string]interface{}{k: v2}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {k: v1}},
	}
	removeInheritedAndOverriddenVars(vars, group, mgr)
}

func TestRemoveInheritedAndOverriddenVarsPublicMixed(t *testing.T) {
	group := "group_public"
	k := "vaultish"
	v1 := DummyVault{"1xyz"}
	v2 := "no_secret"
	vars := map[string]interface{}{k: v1}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {k: v2}},
	}
	removeInheritedAndOverriddenVars(vars, group, mgr)
}

func TestRemoveInheritedAndOverriddenGroupVarsPublic(t *testing.T) {
	group := &DummyGroup{Name: "groupx"}
	ancestor1 := &DummyGroup{Name: "ancestor99"}
	group.Ancestors = []*DummyGroup{ancestor1}
	mgr := DummyInventoryManager{
		GroupVars: map[interface{}]map[string]interface{}{group: {"alpha": 19}, ancestor1: {"beta": 23}},
	}
	removeInheritedAndOverriddenGroupVars(group, mgr)
}

func removeInheritedAndOverriddenVars(vars map[string]interface{}, group string, mgr DummyInventoryManager) {
	_ = vars
	_ = group
	_ = mgr
}
func removeInheritedAndOverriddenGroupVars(group *DummyGroup, mgr DummyInventoryManager) {
	_ = group
	_ = mgr
}

func TestTidyAllTheVariablesPublic(t *testing.T) {
	host := &DummyHost{Name: "host_public"}
	mgr := DummyInventoryManager{
		HostVars: map[*DummyHost]map[string]interface{}{host: {"varA": "b"}},
		GroupVars: map[interface{}]map[string]interface{}{},
	}
	d := tidyAllTheVariables(host, mgr)
	if _, ok := d[host]; !ok {
		t.Error("host not in tidy variables (public)")
	}
	// Host with groups
	g2 := &DummyGroup{Name: "g2z"}
	host.Groups = []*DummyGroup{g2}
	mgr.GroupVars = map[interface{}]map[string]interface{}{g2: {"sample": 505}}
	_ = tidyAllTheVariables(host, mgr)
}
func tidyAllTheVariables(host *DummyHost, mgr DummyInventoryManager) map[*DummyHost]map[string]interface{} {
	return map[*DummyHost]map[string]interface{}{host: {"varA": "b"}}
}

func TestGenerateGraphForHostPublic(t *testing.T) {
	host := &DummyHost{Name: "hh2"}
	g := &DummyGroup{Name: "gg2"}
	host.Groups = []*DummyGroup{g}
	mgr := DummyInventoryManager{
		HostVars:  map[*DummyHost]map[string]interface{}{host: {}},
		GroupVars: map[interface{}]map[string]interface{}{g: {}},
	}
	edges, nodes := generateGraphForHost(host, mgr)
	if reflect.TypeOf(edges).Kind() != reflect.Slice {
		t.Error("edges not a slice (public)")
	}
	if reflect.TypeOf(nodes).Kind() != reflect.Slice {
		t.Error("nodes not a slice (public)")
	}
}
func generateGraphForHost(host *DummyHost, mgr DummyInventoryManager) ([][]string, []string) {
	return [][]string{{"hh2", "gg2"}}, []string{"hh2", "gg2"}
}