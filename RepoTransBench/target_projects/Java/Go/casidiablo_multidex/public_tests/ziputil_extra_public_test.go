package public_tests

import (
	"archive/zip"
	"bytes"
	"testing"
)

func TestZipEntryNoExtraDataPublic(t *testing.T) {
	var b bytes.Buffer
	w := zip.NewWriter(&b)
	fh := &zip.FileHeader{
		Name: "anotherfile.txt",
	}
	f, err := w.CreateHeader(fh)
	if err != nil {
		t.Fatal(err)
	}
	_, err = f.Write([]byte("dummy"))
	if err != nil {
		t.Fatal(err)
	}
	w.Close()

	r, err := zip.NewReader(bytes.NewReader(b.Bytes()), int64(b.Len()))
	if err != nil {
		t.Fatal(err)
	}
	entry := r.File[0]
	if entry.Extra == nil || len(entry.Extra) != 0 {
		// no extra by default
	} else {
		t.Errorf("Expected Extra to be nil or length 0, got %v", entry.Extra)
	}
	entry.Extra = []byte{}
	if entry.Extra == nil || len(entry.Extra) != 0 {
		// still fine
	} else {
		t.Errorf("Expected Extra to be nil or length 0, got %v", entry.Extra)
	}
}

func TestZipEntryWithExtraDataPublic(t *testing.T) {
	var b bytes.Buffer
	w := zip.NewWriter(&b)
	fh := &zip.FileHeader{
		Name: "some_entry.txt",
	}
	extra := []byte{42, 7, 100, 5}
	fh.Extra = extra
	f, err := w.CreateHeader(fh)
	if err != nil {
		t.Fatal(err)
	}
	_, err = f.Write([]byte("dummy"))
	if err != nil {
		t.Fatal(err)
	}
	w.Close()
	r, err := zip.NewReader(bytes.NewReader(b.Bytes()), int64(b.Len()))
	if err != nil {
		t.Fatal(err)
	}
	entry := r.File[0]
	if entry.Extra == nil || len(entry.Extra) != 4 {
		t.Errorf("Expected Extra length 4, got %v", entry.Extra)
	}
	for i := range extra {
		if entry.Extra[i] != extra[i] {
			t.Errorf("Extra array mismatch at %d: got %v want %v", i, entry.Extra[i], extra[i])
		}
	}
}