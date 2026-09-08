package tests

import (
	"os"
	"path/filepath"
	"testing"

	"rbgirshick_yacs/yacs"
)

func TestLoadCfgYamlAndPy(t *testing.T) {
	tmpDir := t.TempDir()
	// YAML file test
	yamlContent := `
A: 123
B:
  C: true
`
	yamlFile := filepath.Join(tmpDir, "test.yaml")
	if err := os.WriteFile(yamlFile, []byte(yamlContent), 0644); err != nil {
		t.Fatalf("Failed to write YAML file: %v", err)
	}
	cfg := yacs.NewEmptyCfgNode(true)
	if err := cfg.MergeFromFile(yamlFile); err != nil {
		t.Fatalf("MergeFromFile YAML failed: %v", err)
	}
	if got := cfg.MustInt("A"); got != 123 {
		t.Errorf("cfg.A: got %v, want 123", got)
	}
	if got := cfg.Node("B").MustBool("C"); got != true {
		t.Errorf("cfg.B.C: got %v, want true", got)
	}

	// Python file test
	pyContent := "cfg = dict(D=456, E=dict(F='bar'))"
	pyFile := filepath.Join(tmpDir, "f.py")
	if err := os.WriteFile(pyFile, []byte(pyContent), 0644); err != nil {
		t.Fatalf("Failed to write py file: %v", err)
	}
	cfg2 := yacs.NewEmptyCfgNode(true)
	if err := cfg2.MergeFromFile(pyFile); err != nil {
		t.Fatalf("MergeFromFile py failed: %v", err)
	}
	if got := cfg2.MustInt("D"); got != 456 {
		t.Errorf("cfg2.D: got %d, want 456", got)
	}
	E := cfg2.Node("E")
	if got := E.MustString("F"); got != "bar" {
		t.Errorf("cfg2.E.F: got %s, want bar", got)
	}
}

func TestLoadCfgFileObjectYaml(t *testing.T) {
	yamlStr := "X: 1\nY: [1,2,3]"
	cn, err := yacs.LoadFromReader(
		yacs.NewStringReader(yamlStr), true)
	if err != nil {
		t.Fatalf("Failed to load from reader: %v", err)
	}
	cfg := yacs.NewEmptyCfgNode(true)
	if err := cfg.MergeFromOther(cn); err != nil {
		t.Fatalf("MergeFromOther failed: %v", err)
	}
	if got := cfg.MustInt("X"); got != 1 {
		t.Errorf("cfg.X: got %d, want 1", got)
	}
	ints := cfg.MustIntSlice("Y")
	if len(ints) != 3 || ints[0] != 1 || ints[1] != 2 || ints[2] != 3 {
		t.Errorf("cfg.Y: got %v, want [1,2,3]", ints)
	}
}

func TestLoadCfgFileObjectPy(t *testing.T) {
	tmpDir := t.TempDir()
	pyContent := "A = [1,2,3]"
	pyFile := filepath.Join(tmpDir, "f.py")
	if err := os.WriteFile(pyFile, []byte(pyContent), 0644); err != nil {
		t.Fatalf("Failed to write py file: %v", err)
	}
	cfgDict := map[string]interface{}{"A": []int{1, 2, 3}}
	cfg := yacs.NewCfgNode(cfgDict, true)
	ints := cfg.MustIntSlice("A")
	if len(ints) != 3 || ints[0] != 1 || ints[1] != 2 || ints[2] != 3 {
		t.Errorf("cfg.A: got %v, want [1,2,3]", ints)
	}
}

func TestDumpAndLoadRoundtrip(t *testing.T) {
	tmpDir := t.TempDir()
	cfg := yacs.NewCfgNode(map[string]interface{}{
		"foo": 3,
		"bar": 6,
	}, false)
	text, err := cfg.Dump()
	if err != nil {
		t.Fatalf("Dump failed: %v", err)
	}
	dumpedFile := filepath.Join(tmpDir, "dumped.yaml")
	if err := os.WriteFile(dumpedFile, []byte(text), 0644); err != nil {
		t.Fatalf("Failed to write YAML: %v", err)
	}
	new_cfg := yacs.NewEmptyCfgNode(true)
	if err := new_cfg.MergeFromFile(dumpedFile); err != nil {
		t.Fatalf("MergeFromFile failed: %v", err)
	}
	if got := new_cfg.MustInt("foo"); got != 3 {
		t.Errorf("new_cfg.foo: got %d, want 3", got)
	}
	if got := new_cfg.MustInt("bar"); got != 6 {
		t.Errorf("new_cfg.bar: got %d, want 6", got)
	}
}

func TestWrongExtension(t *testing.T) {
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "bad.txt")
	if err := os.WriteFile(filePath, []byte("FOO=2"), 0644); err != nil {
		t.Fatalf("Failed to write txt file: %v", err)
	}
	_, err := yacs.LoadCfg(filePath)
	if err == nil {
		t.Errorf("expected error for .txt file, got nil")
	}
}