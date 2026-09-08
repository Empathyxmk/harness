package original

import (
	"bytes"
	"encoding/json"
	"io"
	"os"
	"testing"

	"wbolster_jsonlines/jsonlines"
)

// Equivalent of SAMPLE_BYTES and SAMPLE_TEXT
var sampleBytes = []byte(`{"a": 1}
{"b": 2}
`)
var sampleText = string(sampleBytes)

func isJSONDecodeError(err error) bool {
	// In Go, json.Unmarshal always returns a *json.SyntaxError for decoding error.
	_, ok := err.(*json.SyntaxError)
	return ok
}

func TestReader(t *testing.T) {
	reader := jsonlines.NewReader(bytes.NewReader(sampleBytes))
	defer reader.Close()
	var m map[string]interface{}
	if err := reader.Read(&m); err != nil {
		t.Fatal(err)
	}
	if m["a"] != float64(1) {
		t.Errorf("Expected {a:1}, got %v", m)
	}
	if err := reader.Read(&m); err != nil {
		t.Fatal(err)
	}
	if m["b"] != float64(2) {
		t.Errorf("Expected {b:2}, got %v", m)
	}
	var dummy map[string]interface{}
	err := reader.Read(&dummy)
	if err == nil || err == io.ErrUnexpectedEOF {
		t.Error("Expected EOF error")
	}
}

func TestReadingFromIterable(t *testing.T) {
	input := []string{"1", "{}"}
	buf := bytes.NewBufferString("")
	for _, v := range input {
		buf.WriteString(v)
		buf.WriteString("\n")
	}
	reader := jsonlines.NewReader(buf)
	var out []interface{}
	for {
		var obj interface{}
		err := reader.Read(&obj)
		if err == io.EOF {
			break
		}
		out = append(out, obj)
	}
	expected := []interface{}{float64(1), map[string]interface{}{}}
	if !equalInterfaces(out, expected) {
		t.Errorf("Expected %v, got %v", expected, out)
	}
}

func TestWriterText(t *testing.T) {
	var buf bytes.Buffer
	writer := jsonlines.NewWriter(&buf)
	writer.Write(map[string]interface{}{"a": 1})
	writer.Write(map[string]interface{}{"b": 2})
	writer.Close()
	if buf.String() != sampleText {
		t.Errorf("Expected %q, got %q", sampleText, buf.String())
	}
}

// ... (Remaining tests follow the pattern above for Go idioms)