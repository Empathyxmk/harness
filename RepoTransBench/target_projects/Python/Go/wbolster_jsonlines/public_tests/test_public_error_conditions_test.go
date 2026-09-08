package public_tests

import (
	"bytes"
	"io"
	"os"
	"testing"

	"wbolster_jsonlines/jsonlines"
)

func TestPublicReaderWrongMode(t *testing.T) {
	filePath := "pub_not_existing2.txt"
	defer os.Remove(filePath)
	content := []byte("notjson\nsurely-not-json-either\n")
	if err := os.WriteFile(filePath, content, 0644); err != nil {
		t.Fatal(err)
	}
	f, err := os.Open(filePath)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var got []interface{}
	for {
		var obj interface{}
		err := reader.Read(&obj)
		if err == io.EOF {
			break
		}
		got = append(got, obj)
	}
	// Should be zero because both lines are not valid JSON, all should be skipped/errored
	if len(got) != 0 {
		t.Errorf("Expected no valid objects, got %v", got)
	}
}

func TestPublicWriterWrongMode(t *testing.T) {
	filePath := "pub_myfile_binary.txt"
	defer os.Remove(filePath)
	f, err := os.OpenFile(filePath, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	writer.Write(map[string]interface{}{"write": "to-binary"})
	writer.Close()
	f.Close()
	raw, err := os.ReadFile(filePath)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Contains(raw, []byte(`"write":"to-binary"`)) {
		t.Errorf("Written content did not contain expected string: %q", string(raw))
	}
	if !bytes.HasSuffix(raw, []byte("\n")) {
		t.Error("Written content did not end with a newline")
	}
}

func TestPublicReaderIterable(t *testing.T) {
	input := `{"thing_a": 42}
{"thing_b": [5, 7, 9]}
`
	reader := jsonlines.NewReader(bytes.NewBufferString(input))
	var out []map[string]interface{}
	for {
		var m map[string]interface{}
		err := reader.Read(&m)
		if err == io.EOF {
			break
		}
		out = append(out, m)
	}
	if len(out) != 2 {
		t.Errorf("Expected 2 objects, got %d", len(out))
	}
	if out[0]["thing_a"] != float64(42) {
		t.Errorf("Unexpected value: %v", out[0]["thing_a"])
	}
	if arr, ok := out[1]["thing_b"].([]interface{}); !ok || len(arr) != 3 || arr[1] != float64(7) {
		t.Errorf("Unexpected value: %v", out[1]["thing_b"])
	}
}

func TestPublicWriterNonDict(t *testing.T) {
	filePath := "pub_test2.jsonl"
	defer os.Remove(filePath)
	f, err := os.OpenFile(filePath, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	writer.Write("something completely else")
	writer.Write(3.1415)
	writer.Close()
	f.Close()
	lines, err := os.ReadFile(filePath)
	if err != nil {
		t.Fatal(err)
	}
	lineArr := bytes.Split(lines, []byte("\n"))
	if string(bytes.TrimSpace(lineArr[0])) != `"something completely else"` {
		t.Errorf("First line, got %q", string(lineArr[0]))
	}
	if string(bytes.TrimSpace(lineArr[1])) != "3.1415" {
		t.Errorf("Second line, got %q", string(lineArr[1]))
	}
}

func TestPublicReaderWriterRepr(t *testing.T) {
	filePath := "pub_file2.jsonl"
	defer os.Remove(filePath)
	f, err := os.OpenFile(filePath, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		t.Fatal(err)
	}
	writer := jsonlines.NewWriter(f)
	gotW := writer.String()
	if len(gotW) == 0 {
		t.Errorf("Writer repr empty")
	}
	writer.Close()
	f.Close()
	ff, err := os.Open(filePath)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(ff)
	gotR := reader.String()
	if len(gotR) == 0 {
		t.Errorf("Reader repr empty")
	}
	reader.Close()
	ff.Close()
}

func TestPublicReaderContextManager(t *testing.T) {
	filePath := "pub_lines2.jsonl"
	defer os.Remove(filePath)
	content := `{"fooX_pub": 841}
{"barX_pub": 1881}
`
	os.WriteFile(filePath, []byte(content), 0644)
	f, err := os.Open(filePath)
	if err != nil {
		t.Fatal(err)
	}
	reader := jsonlines.NewReader(f)
	var got []map[string]interface{}
	for {
		var m map[string]interface{}
		err := reader.Read(&m)
		if err == io.EOF {
			break
		}
		got = append(got, m)
	}
	f.Close()
	if len(got) != 2 {
		t.Errorf("Expected 2 JSON maps, got %v", got)
	}
	if got[0]["fooX_pub"] != float64(841) || got[1]["barX_pub"] != float64(1881) {
		t.Errorf("Value mismatch: %v %v", got[0], got[1])
	}
}