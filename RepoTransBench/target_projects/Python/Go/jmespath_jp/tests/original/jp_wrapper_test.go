package original

import (
	"encoding/json"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"testing"
)

// JpWrapper simulates the functionality of jp_wrapper.JpWrapper from Python.
type JpWrapper struct {
	binaryPath string
}

func NewJpWrapper(path string) *JpWrapper {
	return &JpWrapper{binaryPath: path}
}

// Search executes the jp binary with the given query and data, returning the result.
func (w *JpWrapper) Search(query string, data interface{}) (interface{}, error) {
	// Marshal the input data to JSON
	inputJSON, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}

	// Prepare the command: ./jp query
	cmd := exec.Command(w.binaryPath, query)
	cmd.Stdin = bytesReader(inputJSON)

	// Run the command and collect output
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, errors.New(string(output))
	}
	// Try to decode JSON result
	var parsed interface{}
	decErr := json.Unmarshal(output, &parsed)
	if decErr == nil {
		return parsed, nil
	}
	// If not valid JSON, try as a string/int
	var asInt int
	if err := json.Unmarshal(output, &asInt); err == nil {
		return asInt, nil
	}

	// Output may be not JSON but a primitive value (like 1 or "foo"):
	// Try as string directly
	return parsePrimitive(string(output)), nil
}

// Helper: bytes.NewReader (avoiding import cycles)
func bytesReader(b []byte) *os.File {
	tmp := filepath.Join(os.TempDir(), "jp_input_tmp.json")
	os.WriteFile(tmp, b, 0644)
	f, _ := os.Open(tmp)
	return f
}

// Attempts to convert output to int or returns string
func parsePrimitive(out string) interface{} {
	s := out
	// Trim whitespace and quotes
	s = trimString(s)
	// Try as int
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

func TestBasicSelect(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"foo": map[string]interface{}{"bar": 5}}
	result, err := jp.Search("foo.bar", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 5 {
		t.Errorf("expected 5, got %v", result)
	}
}

func TestIdentityQuery(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"foo": 42}
	result, err := jp.Search("@", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	// Compare equivalent map[string]interface{}
	want := map[string]interface{}{"foo": float64(42)}
	if !jsonEqual(result, want) {
		t.Errorf("expected %v, got %v", want, result)
	}
}

func TestListIndex(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"a": []interface{}{1, 2, 3}}
	result, err := jp.Search("a[1]", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 2 && result != float64(2) {
		t.Errorf("expected 2, got %v", result)
	}
}

func TestInvalidQueryRaises(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"foo": 123}
	_, err := jp.Search("???", data)
	if err == nil {
		t.Errorf("expected error for invalid query")
	}
}

func TestNonJsonOutput(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"foo": 1}
	result, err := jp.Search("foo", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	// Accept int or float value
	if result != 1 && result != float64(1) {
		t.Errorf("expected 1, got %v", result)
	}
}

func TestCustomBinaryPath(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"foo": "bar"}
	result, err := jp.Search("foo", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != "bar" {
		t.Errorf("expected 'bar', got %v", result)
	}
}

func TestErrorOnMissingJp(t *testing.T) {
	jp := NewJpWrapper("./missing-jp-bin")
	_, err := jp.Search("foo", map[string]interface{}{"foo": 1})
	if err == nil {
		t.Errorf("expected error searching with missing jp binary")
	}
}

func TestEmptyResult(t *testing.T) {
	skipIfNoJp(t)
	jp := NewJpWrapper("./jp")
	data := map[string]interface{}{"foo": map[string]interface{}{"bar": 123}}
	res, err := jp.Search("foo.baz", data)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	empty := res == nil || (res == "") || (res == "null")
	if !empty {
		t.Errorf("expected nil or empty result for missing path, got %v", res)
	}
}

// Helper for deep JSON equality
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