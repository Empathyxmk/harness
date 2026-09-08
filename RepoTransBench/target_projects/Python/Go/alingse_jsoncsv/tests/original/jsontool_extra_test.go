package original

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"reflect"
	"testing"

	"alingse_jsoncsv/jsoncsv"
)

func TestGenLeafSimpleDict(t *testing.T) {
	root := map[string]interface{}{"a": 1, "b": map[string]interface{}{"c": 2}}
	leaves := jsoncsv.GenLeaf(root)
	foundA, foundBC := false, false
	for _, leaf := range leaves {
		path := leaf.Path
		val := leaf.Value
		if reflect.DeepEqual(path, []string{"a"}) && val == 1 {
			foundA = true
		}
		if reflect.DeepEqual(path, []string{"b", "c"}) && val == 2 {
			foundBC = true
		}
	}
	if !(foundA && foundBC) {
		t.Errorf("expected to find a and b.c leaves")
	}
}

func TestIsArrayIndexTrueAndFalse(t *testing.T) {
	if !jsoncsv.IsArrayIndex([]interface{}{0, 1, 2}) {
		t.Error("expected true")
	}
	if !jsoncsv.IsArrayIndex([]interface{}{1, 0}) {
		t.Error("expected true")
	}
	if !jsoncsv.IsArrayIndex([]interface{}{"0", "1"}) {
		t.Error("expected true")
	}
	if jsoncsv.IsArrayIndex([]interface{}{"a", "b"}) {
		t.Error("expected false")
	}
}

func TestFromLeafDictAndList(t *testing.T) {
	leafs := []jsoncsv.Leaf{
		{Path: []string{"a"}, Value: 1},
		{Path: []string{"b"}, Value: 2},
	}
	v := jsoncsv.FromLeaf(leafs)
	if reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("expected dict/map")
	}
	leafList := []jsoncsv.Leaf{
		{Path: []string{"0"}, Value: "a"},
		{Path: []string{"1"}, Value: "b"},
	}
	v2 := jsoncsv.FromLeaf(leafList)
	if reflect.TypeOf(v2).Kind() != reflect.Slice {
		t.Errorf("expected list/slice")
	}
}

func TestExpandAndRestoreRoundtrip(t *testing.T) {
	d := map[string]interface{}{"a": 1, "b": map[string]interface{}{"c": 2}}
	exp := jsoncsv.Expand(d)
	rest := jsoncsv.Restore(exp)
	if !reflect.DeepEqual(rest, d) {
		t.Errorf("expected %v got %v", d, rest)
	}
}

func TestExpandSafeAndRestoreSafe(t *testing.T) {
	d := map[string]interface{}{"x.y": map[string]interface{}{"z": 1}}
	exp := jsoncsv.ExpandSafe(d)
	rest := jsoncsv.RestoreSafe(exp)
	if !reflect.DeepEqual(rest, d) {
		t.Errorf("expected %v", d)
	}
}

func TestConvertJSONExpandAndRestore(t *testing.T) {
	tmpDir := t.TempDir()
	fdin := filepath.Join(tmpDir, "in.json")
	fdout := filepath.Join(tmpDir, "out.json")
	os.WriteFile(fdin, []byte("{\"x\":1}\n{\"y\":2}\n"), 0644)
	fin, _ := os.Open(fdin)
	fout, _ := os.Create(fdout)
	if err := jsoncsv.ConvertJSON(fin, fout, jsoncsv.Expand, false); err != nil {
		t.Fatal(err)
	}
	fin.Close()
	fout.Close()
	restorePath := filepath.Join(tmpDir, "restore.json")
	fin2, _ := os.Open(fdout)
	fout2, _ := os.Create(restorePath)
	if err := jsoncsv.ConvertJSON(fin2, fout2, jsoncsv.Restore, false); err != nil {
		t.Fatal(err)
	}
	fin2.Close()
	fout2.Close()
	data, _ := os.ReadFile(restorePath)
	for _, line := range bytes.Split(data, []byte("\n")) {
		if len(line) > 0 {
			var obj map[string]interface{}
			json.Unmarshal(line, &obj)
			if reflect.TypeOf(obj).Kind() != reflect.Map {
				t.Errorf("not map/dict: %v", obj)
			}
		}
	}
}

func TestConvertJSONInvalidFunc(t *testing.T) {
	var fin bytes.Buffer
	fin.WriteString("{\"x\":1}\n")
	var fout bytes.Buffer
	err := jsoncsv.ConvertJSON(&fin, &fout, nil, false)
	if err == nil {
		t.Errorf("expected ValueError for nil func")
	}
}

func TestConvertJSONJSONArray(t *testing.T) {
	tmpDir := t.TempDir()
	arr := []map[string]interface{}{
		{"foo": 1},
		{"bar": 2},
	}
	js, _ := json.Marshal(arr)
	fnin := filepath.Join(tmpDir, "arr.json")
	os.WriteFile(fnin, js, 0644)
	fnout := filepath.Join(tmpDir, "outarr.json")
	fin, _ := os.Open(fnin)
	fout, _ := os.Create(fnout)
	if err := jsoncsv.ConvertJSON(fin, fout, jsoncsv.Expand, true); err != nil {
		t.Fatal(err)
	}
	fin.Close()
	fout.Close()
	data, _ := os.ReadFile(fnout)
	lines := bytes.Split(data, []byte("\n"))
	cnt := 0
	for _, l := range lines {
		if len(l) > 0 {
			if !bytes.Contains(l, []byte("foo")) && !bytes.Contains(l, []byte("bar")) {
				t.Errorf("line missing foo or bar")
			}
			cnt++
		}
	}
	if cnt != 2 {
		t.Errorf("expected 2 lines, got %v", cnt)
	}
}