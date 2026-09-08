package public_tests

import (
	"os"
	"path/filepath"
	"testing"

	"rbgirshick_yacs/yacs"
)

func TestLoadCfgYamlAndPy_Public(t *testing.T) {
	tmpDir := t.TempDir()
	// YAML file test - different content
	yamlContent := `
K: 789
L:
  M: false
`
	yamlFile := filepath.Join(tmpDir, "test_diff.yaml")
	if err := os.WriteFile(yamlFile, []byte(yamlContent), 0644); err != nil {
		t.Fatalf("Failed to write YAML file: %v", err)
	}
	cfg := yacs.NewEmptyCfgNode(true)
	if err := cfg.MergeFromFile(yamlFile); err != nil {
		t.Fatalf("MergeFromFile YAML failed: %v", err)
	}
	if got := cfg.MustInt("K"); got != 789 {
		t.Errorf("cfg.K: got %d, want 789", got)
	}
	if got := cfg.Node("L").MustBool("M"); got != false {
		t.Errorf("cfg.L.M: got %v, want false", got)
	}

	// Python file test (must define variable 'cfg' at top-level!)
	pyContent := "cfg = dict(Z=[7,8,9], Y=dict(X='baz'))"
	pyFile := filepath.Join(tmpDir, "f2.py")
	if err := os.WriteFile(pyFile, []byte(pyContent), 0644); err != nil {
		t.Fatalf("Failed to write py file: %v", err)
	}
	cfg2 := yacs.NewEmptyCfgNode(true)
	if err := cfg2.MergeFromFile(pyFile); err != nil {
		t.Fatalf("MergeFromFile py failed: %v", err)
	}
	z, ok := cfg2.AsMap()["Z"]
	if !ok {
		t.Fatalf("cfg2.Z missing")
	}
	ints := []int{}
	switch arr := z.(type) {
	case []int:
		ints = arr
	case []interface{}:
		for _, x := range arr {
			switch v := x.(type) {
			case int:
				ints = append(ints, v)
			case int64:
				ints = append(ints, int(v))
			case float64:
				ints = append(ints, int(v))
			}
		}
	}
	if len(ints) != 3 || ints[0] != 7 || ints[1] != 8 || ints[2] != 9 {
		t.Errorf("cfg2.Z: got %v, want [7,8,9]", ints)
	}
	yV, ok := cfg2.AsMap()["Y"]
	if !ok {
		t.Fatalf("cfg2.Y missing")
	}
	var ysub map[string]interface{}
	switch y := yV.(type) {
	case map[string]interface{}:
		ysub = y
	case *yacs.CfgNode:
		ysub = y.AsMap()
	}
	x, ok := ysub["X"]
	if !ok || x != "baz" {
		t.Errorf("cfg2.Y.X: got %v, want baz", x)
	}
}

func TestLoadCfgFileObjectYaml_Public(t *testing.T) {
	yamlStr := "A: 88\nB: [4, 5, 6]"
	reader := yacs.NewStringReader(yamlStr)
	cn, err := yacs.LoadFromReader(reader, true)
	if err != nil {
		t.Fatalf("LoadFromReader: %v", err)
	}
	cfg := yacs.NewEmptyCfgNode(true)
	if err := cfg.MergeFromOther(cn); err != nil {
		t.Fatalf("MergeFromOther failed: %v", err)
	}
	if got := cfg.MustInt("A"); got != 88 {
		t.Errorf("cfg.A: got %d, want 88", got)
	}
	ints := cfg.MustIntSlice("B")
	if len(ints) != 3 || ints[0] != 4 || ints[1] != 5 || ints[2] != 6 {
		t.Errorf("cfg.B: got %v, want [4,5,6]", ints)
	}
}

func TestLoadCfgFileObjectPy_Public(t *testing.T) {
	tmpDir := t.TempDir()
	pyContent := "ALPHA = [100,200,300]"
	pyFile := filepath.Join(tmpDir, "f_obj.py")
	if err := os.WriteFile(pyFile, []byte(pyContent), 0644); err != nil {
		t.Fatalf("Failed to write py file: %v", err)
	}
	cfgDict := map[string]interface{}{"ALPHA": []int{100, 200, 300}}
	cfg := yacs.NewCfgNode(cfgDict, true)
	ints := cfg.MustIntSlice("ALPHA")
	if len(ints) != 3 || ints[0] != 100 || ints[1] != 200 || ints[2] != 300 {
		t.Errorf("cfg.ALPHA: got %v, want [100,200,300]", ints)
	}
}

func TestDumpAndLoadRoundtrip_Public(t *testing.T) {
	tmpDir := t.TempDir()
	cfg := yacs.NewCfgNode(map[string]interface{}{
		"foo": 21,
		"bar": "hello world",
	}, false)
	text, err := cfg.Dump()
	if err != nil {
		t.Fatalf("Dump failed: %v", err)
	}
	dumpedFile := filepath.Join(tmpDir, "public_dumped.yaml")
	if err := os.WriteFile(dumpedFile, []byte(text), 0644); err != nil {
		t.Fatalf("Failed to write YAML: %v", err)
	}
	new_cfg := yacs.NewEmptyCfgNode(true)
	if err := new_cfg.MergeFromFile(dumpedFile); err != nil {
		t.Fatalf("MergeFromFile failed: %v", err)
	}
	if got := new_cfg.MustInt("foo"); got != 21 {
		t.Errorf("new_cfg.foo: got %d, want 21", got)
	}
	if got := new_cfg.MustString("bar"); got != "hello world" {
		t.Errorf("new_cfg.bar: got %s, want 'hello world'", got)
	}
}

func TestWrongExtension_Public(t *testing.T) {
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "bad2.txt")
	if err := os.WriteFile(filePath, []byte("BAR=3"), 0644); err != nil {
		t.Fatalf("Failed to write txt file: %v", err)
	}
	_, err := yacs.LoadCfg(filePath)
	if err == nil {
		t.Errorf("expected error for .txt file, got nil")
	}
}