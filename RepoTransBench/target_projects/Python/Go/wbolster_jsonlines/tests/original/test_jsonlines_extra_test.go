package original

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"os"
	"testing"

	"wbolster_jsonlines/jsonlines"
)

func TestDefaultDumpsNotImplemented(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic on DefaultDumps, but did not panic")
		}
	}()
	_ = jsonlines.DefaultDumps(nil)
}

func TestInvalidLineErrorProperties(t *testing.T) {
	err := jsonlines.NewInvalidLineError("Bad", "bad json line", 3)
	if _, ok := err.(error); !ok {
		t.Errorf("Should be an error")
	}
	if err.Line != "bad json line" {
		t.Errorf("Expected line to be 'bad json line', got %q", err.Line)
	}
	if err.Lineno != 3 {
		t.Errorf("Expected lineno to be 3, got %v", err.Lineno)
	}
	if got := err.Error(); !contains(got, "Bad") {
		t.Errorf("Expected error string to contain 'Bad'")
	}
	err2 := jsonlines.NewInvalidLineError("Test", "line\n", 5)
	if err2.Line != "line" {
		t.Errorf("Expected line to be 'line', got %q", err2.Line)
	}
}

func TestReaderWriterBaseCloseCalledMultipleTimes(t *testing.T) {
	base := jsonlines.NewReaderWriterBase()
	base.Close()
	base.Close()
}

func TestReaderWriterBaseEq(t *testing.T) {
	base1 := jsonlines.NewReaderWriterBase()
	base2 := jsonlines.NewReaderWriterBase()
	if !base1.Equal(base2) {
		t.Errorf("Two ReaderWriterBase objects should be equal")
	}
}

func TestWriterWriteObjTypes(t *testing.T) {
	path := "test.jsonl"
	defer os.Remove(path)
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	writer := jsonlines.NewWriter(f)
	err = writer.Write(map[string]interface{}{"k": 1})
	if err != nil {
		t.Fatal(err)
	}
	f.Sync()
	f.Seek(0, io.SeekStart)
	reader := jsonlines.NewReader(f)
	var items []map[string]interface{}
	for {
		var m map[string]interface{}
		err := reader.Read(&m)
		if errors.Is(err, io.EOF) {
			break
		}
		if err != nil {
			t.Fatal(err)
		}
		items = append(items, m)
	}
	reader.Close()
	writer.Close()
	if len(items) != 1 || items[0]["k"] != float64(1) {
		t.Errorf("Expected one item [{'k': 1}], got %#v", items)
	}
}

func TestWriterWritesSupportedTypes(t *testing.T) {
	path := "test2.jsonl"
	defer os.Remove(path)
	data := []interface{}{
		map[string]interface{}{"a": 1},
		[]interface{}{1, 2, 3},
		1,
		2.5,
		true,
		"hello",
	}
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	writer := jsonlines.NewWriter(f)
	for _, item := range data {
		if err := writer.Write(item); err != nil {
			t.Fatalf("Error writing: %v", err)
		}
	}
	writer.Close()
	f2, _ := os.Open(path)
	defer f2.Close()
	reader := jsonlines.NewReader(f2)
	var got []interface{}
	for {
		var obj interface{}
		err := reader.Read(&obj)
		if errors.Is(err, io.EOF) {
			break
		}
		if err != nil {
			t.Fatal(err)
		}
		got = append(got, obj)
	}
	reader.Close()
	if !equalInterfaces(got, data) {
		t.Errorf("Expected %v, got %v", data, got)
	}
}

func TestWriterWriteUnsupportedType(t *testing.T) {
	path := "test3.jsonl"
	defer os.Remove(path)
	type C struct{}
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()

	writer := jsonlines.NewWriter(f)
	err = writer.Write(C{})
	if err == nil {
		t.Error("Expected error when writing unsupported type")
	}
}

func TestWriterClose(t *testing.T) {
	path := "test_flush.jsonl"
	defer os.Remove(path)
	f, err := os.Create(path)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	err = writer.Write(map[string]interface{}{"a": 1})
	if err != nil {
		t.Fatal(err)
	}
	writer.Close()
	f.Close()
}

func TestReaderValidAndEOF(t *testing.T) {
	text := `{"a":1}
{"b":2}
`
	path := "test_read.jsonl"
	defer os.Remove(path)
	os.WriteFile(path, []byte(text), 0644)
	f, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var a, b map[string]interface{}
	if err := reader.Read(&a); err != nil {
		t.Fatal(err)
	}
	if err := reader.Read(&b); err != nil {
		t.Fatal(err)
	}
	var dummy map[string]interface{}
	if err := reader.Read(&dummy); !errors.Is(err, io.EOF) {
		t.Errorf("Expected EOFError on third read, got %v", err)
	}
	reader.Close()
	reader.Close()
	f.Close()
}

func TestReaderInvalidLine(t *testing.T) {
	path := "test_inv.jsonl"
	defer os.Remove(path)
	os.WriteFile(path, []byte(`{"a":1}
notjson
`), 0644)
	f, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var a map[string]interface{}
	if err := reader.Read(&a); err != nil {
		t.Fatal(err)
	}
	var dummy interface{}
	err = reader.Read(&dummy)
	if err == nil {
		t.Errorf("Expected error for invalid line")
	} else if !contains(err.Error(), "notjson") && !contains(err.Error(), "invalid json") {
		t.Errorf("Expected error message to contain 'notjson' or 'invalid json', got %v", err)
	}
	reader.Close()
	f.Close()
}

func TestReaderSkipInitialChar(t *testing.T) {
	path := "test_skip.jsonl"
	defer os.Remove(path)
	bom := []byte{0xef, 0xbb, 0xbf}
	row := append(bom, []byte(`{"x": 1}
`)...)
	os.WriteFile(path, row, 0644)
	f, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var v map[string]interface{}
	if err := reader.Read(&v); err != nil {
		t.Fatalf("Failed to read BOM line: %v", err)
	}
	if x, ok := v["x"]; !ok || x != float64(1) {
		t.Errorf("Expected x==1")
	}
	var dummy map[string]interface{}
	if err := reader.Read(&dummy); !errors.Is(err, io.EOF) {
		t.Errorf("Expected EOFError, got %v", err)
	}
	reader.Close()
	f.Close()
}

func TestWriterModeBytes(t *testing.T) {
	path := "test_bytes.jsonl"
	defer os.Remove(path)
	f, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR, 0666)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	err = writer.Write(map[string]interface{}{"k": 42})
	if err != nil {
		t.Fatal(err)
	}
	writer.Close()
	f.Close()
	fb, _ := os.Open(path)
	defer fb.Close()
	reader := jsonlines.NewReader(fb)
	var v map[string]interface{}
	if err := reader.Read(&v); err != nil {
		t.Fatal(err)
	}
	if v["k"] != float64(42) {
		t.Errorf("Expected k==42")
	}
	var dummy map[string]interface{}
	if err := reader.Read(&dummy); !errors.Is(err, io.EOF) {
		t.Errorf("Expected EOF, got %v", err)
	}
	reader.Close()
}

func TestOpenFunctionModes(t *testing.T) {
	fpath := "openf.jsonl"
	defer os.Remove(fpath)
	writer, err := jsonlines.Open(fpath, "w")
	if err != nil {
		t.Fatal(err)
	}
	writer.Write(map[string]interface{}{"value": 42})
	writer.Close()

	reader, err := jsonlines.Open(fpath, "r")
	if err != nil {
		t.Fatal(err)
	}
	var v map[string]interface{}
	if err := reader.Read(&v); err != nil {
		t.Fatalf("Read: %v", err)
	}
	if v["value"] != float64(42) {
		t.Errorf("Expected value=42, got %v", v["value"])
	}
	reader.Close()
}

// Supporting helpers

func contains(s, substr string) bool {
	return bytes.Contains([]byte(s), []byte(substr))
}

func equalInterfaces(a, b []interface{}) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		atypestr := typeOf(a[i])
		btypestr := typeOf(b[i])
		if atypestr != btypestr {
			return false
		}
		switch av := a[i].(type) {
		case float64, string, bool:
			if av != b[i] {
				return false
			}
		case map[string]interface{}:
			bv, ok := b[i].(map[string]interface{})
			if !ok {
				return false
			}
			ajson, _ := json.Marshal(av)
			bjson, _ := json.Marshal(bv)
			if !bytes.Equal(ajson, bjson) {
				return false
			}
		case []interface{}:
			bv, ok := b[i].([]interface{})
			if !ok {
				return false
			}
			if !equalInterfaces(av, bv) {
				return false
			}
		default:
			return false
		}
	}
	return true
}

func typeOf(x interface{}) string {
	switch x.(type) {
	case map[string]interface{}:
		return "map"
	case []interface{}:
		return "slice"
	case string:
		return "string"
	case float64:
		return "float"
	case bool:
		return "bool"
	default:
		return "unknown"
	}
}

func TestReaderWriterBaseContextManager(t *testing.T) {
	b := jsonlines.NewReaderWriterBase()
	b.Enter()
	b.Close()
	b.Exit(nil, nil, nil)
}