package public_tests

import (
	"bytes"
	"encoding/json"
	"io"
	"testing"

	"wbolster_jsonlines/jsonlines"
)

func TestPublicTypingWithReader(t *testing.T) {
	r := jsonlines.NewReader(bytes.NewReader([]byte(`"newtext"`)))
	var s string
	if err := r.Read(&s); err != nil {
		t.Error(err)
	}
	r = jsonlines.NewReader(bytes.NewReader([]byte(`"newbytes"`)))
	if err := r.Read(&s); err != nil {
		t.Error(err)
	}
	// test type handling; for Go, just try int, float64, bool, string, map, slice
	var n int
	if err := r.Read(&n); err != nil {
		t.Error(err)
	}
	var f float64
	if err := r.Read(&f); err != nil {
		t.Error(err)
	}
	var b bool
	if err := r.Read(&b); err != nil {
		t.Error(err)
	}
	var m map[string]interface{}
	if err := r.Read(&m); err != nil {
		t.Error(err)
	}
	var list []interface{}
	if err := r.Read(&list); err != nil {
		t.Error(err)
	}
}

func TestPublicTypingWithWriter(t *testing.T) {
	w := jsonlines.NewWriter(io.Discard)
	if err := w.Write("abc"); err != nil {
		t.Error(err)
	}
	if err := w.Write(123); err != nil {
		t.Error(err)
	}
	w.Close()
}

func TestPublicTypingWithOpen(t *testing.T) {
	name := "/dev/null"
	_, err := jsonlines.Open(name, "r")
	if err != nil && !isNoFileError(err) {
		t.Errorf("Open for read failed: %v", err)
	}
	_, err = jsonlines.Open(name, "w")
	if err != nil && !isNoFileError(err) {
		t.Errorf("Open for write failed: %v", err)
	}
}

func isNoFileError(err error) bool {
	return err != nil && (err.Error() == "no such file or directory" || err.Error() == "file does not exist")
}