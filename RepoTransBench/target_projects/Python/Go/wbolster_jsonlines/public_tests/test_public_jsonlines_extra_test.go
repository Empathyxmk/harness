package public_tests

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"os"
	"testing"

	"wbolster_jsonlines/jsonlines"
)

func TestPublicDefaultDumpsNotImplemented(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic on DefaultDumps")
		}
	}()
	_ = jsonlines.DefaultDumps(123)
}

func TestPublicInvalidLineErrorProperties(t *testing.T) {
	err := jsonlines.NewInvalidLineError("Oops", "another bad json", 7)
	if _, ok := err.(error); !ok {
		t.Errorf("Should be error")
	}
	if err.Line != "another bad json" {
		t.Errorf("Line mismatch, got %q", err.Line)
	}
	if err.Lineno != 7 {
		t.Errorf("Expected lineno 7, got %v", err.Lineno)
	}
	if got := err.Error(); !contains(got, "Oops") {
		t.Errorf("Error string doesn't contain 'Oops'")
	}
	err2 := jsonlines.NewInvalidLineError("Msg", "lineagain\n", 4)
	if err2.Line != "lineagain" {
		t.Errorf("Expected 'lineagain', got %q", err2.Line)
	}
}

func TestPublicReaderWriterBaseCloseMultiple(t *testing.T) {
	base := jsonlines.NewReaderWriterBase()
	base.Close()
	base.Close()
}

func TestPublicReaderWriterBaseEq(t *testing.T) {
	a := jsonlines.NewReaderWriterBase()
	b := jsonlines.NewReaderWriterBase()
	if !a.Equal(b) {
		t.Error("Base objects should be equal")
	}
}

func TestPublicWriterWriteObjTypes(t *testing.T) {
	path := "public_test.jsonl"
	defer os.Remove(path)
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	writer := jsonlines.NewWriter(f)
	if err := writer.Write(map[string]interface{}{"xyz": 15}); err != nil {
		t.Errorf("Write err: %v", err)
	}
	f.Sync()
	f.Seek(0, io.SeekStart)
	reader := jsonlines.NewReader(f)
	items := []map[string]interface{}{}
	for {
		var m map[string]interface{}
		err := reader.Read(&m)
		if errors.Is(err, io.EOF) {
			break
		}
		items = append(items, m)
	}
	reader.Close()
	if len(items) != 1 || items[0]["xyz"] != float64(15) {
		t.Errorf("Expected [{'xyz':15}], got %v", items)
	}
}

func TestPublicWriterWritesSupportedTypes(t *testing.T) {
	path := "public_test2.jsonl"
	defer os.Remove(path)
	data := []interface{}{
		map[string]interface{}{"foo": 9},
		[]interface{}{float64(5), float64(4)},
		7,
		0.1,
		false,
		"world",
	}
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	writer := jsonlines.NewWriter(f)
	for _, val := range data {
		if err := writer.Write(val); err != nil {
			t.Fatalf("Fail write: %v", err)
		}
	}
	writer.Close()

	ff, _ := os.Open(path)
	defer ff.Close()
	reader := jsonlines.NewReader(ff)
	var got []interface{}
	for {
		var v interface{}
		err := reader.Read(&v)
		if errors.Is(err, io.EOF) {
			break
		}
		got = append(got, v)
	}
	reader.Close()
	if !equalInterfaces(got, data) {
		t.Errorf("Expected %v, got %v", data, got)
	}
}

func TestPublicWriterWriteUnsupportedType(t *testing.T) {
	path := "public_test3.jsonl"
	defer os.Remove(path)
	type D struct{}
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	writer := jsonlines.NewWriter(f)
	err = writer.Write(D{})
	if err == nil {
		t.Errorf("Expected error writing unsupported type")
	}
}

func TestPublicWriterClose(t *testing.T) {
	path := "public_flush.jsonl"
	defer os.Remove(path)
	f, err := os.Create(path)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	writer.Write(map[string]interface{}{"bar": 10})
	writer.Close()
	f.Close()
}

func TestPublicReaderValidAndEOF(t *testing.T) {
	text := `{"x":42}
{"y":77}
`
	path := "public_read.jsonl"
	defer os.Remove(path)
	os.WriteFile(path, []byte(text), 0644)
	f, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var x, y map[string]interface{}
	if err := reader.Read(&x); err != nil {
		t.Fatal(err)
	}
	if x["x"] != float64(42) {
		t.Errorf("Missed value x")
	}
	if err := reader.Read(&y); err != nil {
		t.Fatal(err)
	}
	if y["y"] != float64(77) {
		t.Errorf("Missed value y")
	}
	var dummy map[string]interface{}
	if err := reader.Read(&dummy); !errors.Is(err, io.EOF) {
		t.Errorf("Expected EOF, got %v", err)
	}
	reader.Close()
	f.Close()
}

func TestPublicReaderInvalidLine(t *testing.T) {
	path := "public_inv.jsonl"
	defer os.Remove(path)
	os.WriteFile(path, []byte(`{"key":5}
NOTJSON
`), 0644)
	f, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var obj map[string]interface{}
	err = reader.Read(&obj)
	if err != nil {
		t.Fatalf("Err: %v", err)
	}
	var dummy interface{}
	err = reader.Read(&dummy)
	if err == nil {
		t.Errorf("Expected error")
	} else if !contains(err.Error(), "NOTJSON") && !contains(err.Error(), "invalid json") {
		t.Errorf("Unexpected err: %v", err)
	}
	reader.Close()
	f.Close()
}

func TestPublicReaderSkipInitialChar(t *testing.T) {
	path := "public_skip.jsonl"
	defer os.Remove(path)
	bom := []byte{0xef, 0xbb, 0xbf}
	row := append(bom, []byte(`{"z": 123}
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
	if v["z"] != float64(123) {
		t.Errorf("Expected z==123")
	}
	var dummy map[string]interface{}
	if err := reader.Read(&dummy); !errors.Is(err, io.EOF) {
		t.Errorf("Expected EOF, got %v", err)
	}
	reader.Close()
	f.Close()
}

func TestPublicWriterModeBytes(t *testing.T) {
	path := "public_bytes.jsonl"
	defer os.Remove(path)
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	writer.Write(map[string]interface{}{"val": 108})
	writer.Close()
	f.Close()
	fb, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	defer fb.Close()
	reader := jsonlines.NewReader(fb)
	var v map[string]interface{}
	err = reader.Read(&v)
	if err != nil {
		t.Fatal(err)
	}
	if v["val"] != float64(108) {
		t.Errorf("Expected val==108")
	}
	var dummy map[string]interface{}
	if err := reader.Read(&dummy); !errors.Is(err, io.EOF) {
		t.Errorf("Expected EOF")
	}
	reader.Close()
}

func TestPublicOpenFunctionModes(t *testing.T) {
	fpath := "public_openf.jsonl"
	defer os.Remove(fpath)
	writer, err := jsonlines.Open(fpath, "w")
	if err != nil {
		t.Fatal(err)
	}
	writer.Write(map[string]interface{}{"value": 73})
	writer.Close()
	reader, err := jsonlines.Open(fpath, "r")
	if err != nil {
		t.Fatal(err)
	}
	var v map[string]interface{}
	if err := reader.Read(&v); err != nil {
		t.Fatalf("Read: %v", err)
	}
	if v["value"] != float64(73) {
		t.Errorf("Expected value=73, got %v", v["value"])
	}
	reader.Close()
}

func TestPublicReaderWriterBaseContextManager(t *testing.T) {
	b := jsonlines.NewReaderWriterBase()
	b.Enter()
	b.Close()
	b.Exit(nil, nil, nil)
}

// Helpers
func contains(hay, needle string) bool {
	return bytes.Contains([]byte(hay), []byte(needle))
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
			aj, _ := json.Marshal(av)
			bj, _ := json.Marshal(bv)
			if !bytes.Equal(aj, bj) {
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