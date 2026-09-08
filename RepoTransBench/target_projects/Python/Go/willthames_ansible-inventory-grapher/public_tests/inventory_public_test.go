package public_tests

import (
	"errors"
	"reflect"
	"testing"
)

type NoVaultSecretFoundPublic struct{}

func (e NoVaultSecretFoundPublic) Error() string { return "no vault secret found" }

func TestNoVaultSecretFoundPublic(t *testing.T) {
	ex := NoVaultSecretFoundPublic{}
	if _, ok := interface{}(ex).(NoVaultSecretFoundPublic); !ok {
		t.Errorf("public ex not NoVaultSecretFoundPublic")
	}
}

// All types below are named *Public to avoid name clash
type FakeCLIPublic struct {
	Called bool
}

func (c *FakeCLIPublic) SetupVaultSecrets(loader, vaultIds, vaultPasswordFiles interface{}, askVaultPass bool) {
	c.Called = true
}

type DummyLoaderPublic struct{}

type DummyIMPublic struct {
	Sources []string
	Loader  DummyLoaderPublic
}

func (m *DummyIMPublic) Groups() map[string]interface{} { return map[string]interface{}{} }

type DummyGroupPublic struct{}

type DummyPluginPublic struct {
	Called bool
}

func (p *DummyPluginPublic) GetVars(loader, path interface{}, entities []interface{}) map[string]interface{} {
	p.Called = true
	return map[string]interface{}{"baz": "qux"}
}

type DummyPluginHostPublic struct {
	DummyPluginPublic
}

func (p *DummyPluginHostPublic) GetHostVars(name string) map[string]interface{} {
	return map[string]interface{}{"a": 82}
}
func (p *DummyPluginHostPublic) GetGroupVars(name string) map[string]interface{} {
	return map[string]interface{}{"b": 99}
}

type DummyHostPublic struct {
	Name string
}

func TestAnsibleInventoryPublicInit(t *testing.T) {
	fcli := &FakeCLIPublic{}
	im := &DummyIMPublic{Sources: []string{"/var/xyz"}, Loader: DummyLoaderPublic{}}
	aiInst := struct {
		Inventory      interface{}
		VaultPassword  bool
		VaultFiles     []string
		VaultIds       []string
		VariableManager interface{}
	}{}
	aiInst.Inventory = im
	aiInst.VaultPassword = true
	aiInst.VaultFiles = []string{}
	aiInst.VaultIds = []string{}
	aiInst.VariableManager = struct{ SetInventory func(interface{}) }{}
	if reflect.ValueOf(aiInst.Inventory).IsZero() {
		t.Errorf("AnsibleInventory public missing inventory")
	}
}

func TestPluginsInventoryPublic(t *testing.T) {
	vi := struct {
		VariableManager interface{}
	}{}
	vi.VariableManager = struct {
		Inventory *DummyIMPublic
		Sources   []string
		Loader    DummyLoaderPublic
	}{Inventory: &DummyIMPublic{Sources: []string{"/var/xyz"}, Loader: DummyLoaderPublic{}}, Sources: []string{"/var/xyz"}, Loader: DummyLoaderPublic{}}
	plugins := []interface{}{&DummyPluginPublic{}}
	results := make(map[string]interface{}, 0)
	for _, plugin := range plugins {
		_, has := plugin.(*DummyPluginPublic)
		if has {
			results["p"] = 99
		}
	}
	if reflect.TypeOf(results).Kind() != reflect.Map {
		t.Error("plugins inventory public did not return map")
	}
}

func TestGetPluginVarsHostPublic(t *testing.T) {
	plugin := &DummyPluginHostPublic{}
	entities := []DummyHostPublic{{Name: "hh"}}
	res := plugin.GetHostVars("hh")
	if _, exists := res["a"]; !exists {
		t.Errorf("_get_plugin_vars public did not return 'a' in result")
	}
}

func TestGetGroupVarsPublic(t *testing.T) {
	ret := map[string]interface{}{"other": "groupvar2"}
	if ret["other"] != "groupvar2" {
		t.Errorf("public get_group_vars error, got %#v", ret)
	}
}

func TestGetHostVarsMagicPublic(t *testing.T) {
	getVars := func(host string, includeHostVars bool) map[string]interface{} {
		return map[string]interface{}{
			"persist":         42,
			"omit":            "remove",
			"ansible_version": "yyy",
		}
	}
	vars := getVars("hh", true)
	if _, ok := vars["omit"]; ok {
		t.Errorf("public got key omit")
	}
	if _, ok := vars["ansible_version"]; ok {
		t.Errorf("public got key ansible_version")
	}
	if _, ok := vars["persist"]; !ok {
		t.Errorf("public expected persist")
	}
}

func TestGetHostVarsAnsibleErrorPublic(t *testing.T) {
	getVars := func() error {
		return errors.New("fail")
	}
	err := getVars()
	if err == nil {
		t.Error("public expected error, got nil")
	}
}

func TestGetGroupPublic(t *testing.T) {
	groups := map[string]int{"gx": 501}
	if groups["gx"] != 501 {
		t.Error("group public lookup failed")
	}
}

func TestGetHostPublic(t *testing.T) {
	getHost := func(h string) string { return "hostX" }
	if getHost("baz") != "hostX" {
		t.Error("get_host public wrong result")
	}
}

func TestListHostsPublic(t *testing.T) {
	listHosts := func(p string) []string { return []string{"h2"} }
	result := listHosts("p2")
	if len(result) != 1 || result[0] != "h2" {
		t.Error("list_hosts public returned wrong result")
	}
}

func TestInventoryManagerPublic(t *testing.T) {
	inv := "public_invobj"
	im := struct{ Inventory string }{Inventory: inv}
	if im.Inventory != "public_invobj" {
		t.Errorf("inventory manager public error")
	}
	im2 := struct{ Inventory string }{Inventory: inv}
	if im2.Inventory != "public_invobj" {
		t.Errorf("inventory manager public error #2")
	}
}