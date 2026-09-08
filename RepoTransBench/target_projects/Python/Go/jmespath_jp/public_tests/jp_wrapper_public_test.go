package public_tests

import (
	"encoding/json"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"fmt"
)

// JpWrapper simulates the functionality of jp_wrapper.JpWrapper from Python.
type JpWrapper struct {
	binaryPath string
}

func NewJpWrapper(path string) *JpWrapper {
	return &JpWrapper{binaryPath: path}
}

func (w *JpWrapper) Search(query string, data interface{}) (interface{}, error) {
	inputJSON, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}

	cmd := exec.Command(w.binaryPath, query)
	cmd.Stdin = bytesReader(inputJSON)

	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, errors.New(string(output))
	}
	var parsed interface{}
	decErr := json.Unmarshal(output, &parsed)
	if decErr == nil {
		return parsed, nil
	}
	var asInt int
	if err := json.Unmarshal(output, &asInt); err == nil {
		return asInt, nil
	}

	return parsePrimitive(string(output)), nil
}

func bytesReader(b []byte) *os.File {
	tmp := filepath.Join(os.TempDir(), "jp_input_tmp_public.json")
	os.WriteFile(tmp, b, 0644)
	f, _ := os.Open(tmp)
	return f
}

func parsePrimitive(out string) interface{} {
	s := out
	s = trimString(s)
	var intVal int
	if _, err := fmt.Sscanf(s, "%d", &intVal); err == nil {
		return intVal
	}
	return s
}

func trimString(s string) string {
	s = strings.TrimSpace(s)
	s = strings.TrimPrefix(s, "\"")
	s = strings.TrimSuffix(s, "\"")
	return s
}

func jpExists() bool {
	info, err := os.Stat("./jp")
	if err != nil {
		return false
	}
	return info.Mode().IsRegular() && (info.Mode().Perm()&0100 != 0)
}

func skipIfNoJp(t *testing.T) {
	if !jpExists() {
		t.Skip("jp binary not available for wrapper tests")
	}
}

func TestPublicBasicSelect(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"alpha": map[string]interface{}{"beta": 9}}
	result, err := jp.Search("alpha.beta", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 9 && result != float64(9) {
		t.Errorf("expected 9, got %v", result)
	}
}

func TestPublicIdentityQuery(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"bar": 17}
	result, err := jp.Search("@", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := map[string]interface{}{"bar": float64(17)}
	if !jsonEqual(result, want) {
		t.Errorf("expected %v, got %v", want, result)
	}
}

func TestPublicListIndex(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"numbers": []interface{}{10, 20, 30}}
	result, err := jp.Search("numbers[2]", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 30 && result != float64(30) {
		t.Errorf("expected 30, got %v", result)
	}
}

func TestPublicInvalidQueryRaises(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"bar": 987}
	_, err := jp.Search("!!!", data)
	if err == nil {
		t.Errorf("expected error for invalid query")
	}
}

func TestPublicNonJsonOutput(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"bar": 7}
	result, err := jp.Search("bar", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 7 && result != float64(7) {
		t.Errorf("expected 7, got %v", result)
	}
}

func TestPublicCustomBinaryPath(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"a": "b"}
	result, err := jp.Search("a", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != "b" {
		t.Errorf("expected 'b', got %v", result)
	}
}

func TestPublicErrorOnMissingJp(t *testing.T) {
	jp := NewJpWrapper("./not-found-jp-bin")
	_, err := jp.Search("bar", map[string]interface{}{"bar": 4})
	if err == nil {
		t.Errorf("expected error searching with missing jp binary")
	}
}

func TestPublicEmptyResult(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"alpha": map[string]interface{}{"beta": 1234}}
	res, err := jp.Search("alpha.gamma", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	empty := res == nil || (res == "") || (res == "null")
	if !empty {
		t.Errorf("expected nil or empty result for missing path, got %v", res)
	}
}


func jsonEqual(a, b interface{}) bool {
	ab, err := json.Marshal(a)
	if err != nil {
		return false
	}
	bb, err := json.Marshal(b)
	if err != nil {
		return false
	}
	return string(ab) == string(bb)
}