package original

import (
	"archive/zip"
	"bytes"
	"errors"
	"testing"
)

// Simulating mailmerge.MailMerge constructor
// In place of real DOCX parsing, just check zip validity & that required files exist.
type MailMerge struct {
	data []byte
}

func NewMailMerge(data []byte) (*MailMerge, error) {
	rd, err := zip.NewReader(bytes.NewReader(data), int64(len(data)))
	if err != nil {
		return nil, err
	}
	foundCT := false
	for _, f := range rd.File {
		if f.Name == "[Content_Types].xml" {
			foundCT = true
			break
		}
	}
	if !foundCT {
		return nil, errors.New("missing [Content_Types].xml")
	}
	return &MailMerge{data: data}, nil
}

func TestCtorInvalidZip(t *testing.T) {
	// Not a valid DOCX/zip file, must raise a BadZipFile (simulated as zip.ErrFormat)
	broken := []byte("notazipfile")
	_, err := NewMailMerge(broken)
	if err == nil {
		t.Fatalf("Expected error for invalid zip data, got nil")
	}
	var zipErr *zip.ReadError
	if !errors.Is(err, zip.ErrFormat) && !errors.As(err, &zipErr) {
		t.Fatalf("Expected zip format error, got: %v", err)
	}
}

func TestCtorContentTypesMissing(t *testing.T) {
	// Create in-memory zip file but missing the '[Content_Types].xml' part
	buf := new(bytes.Buffer)
	zipWriter := zip.NewWriter(buf)
	_, err := zipWriter.Create("word/document.xml")
	if err != nil {
		t.Fatalf("unexpected error creating zip entry: %v", err)
	}
	zipWriter.Close()
	_, err = NewMailMerge(buf.Bytes())
	if err == nil {
		t.Fatalf("Expected error for missing [Content_Types].xml, got nil")
	}
	if err.Error() != "missing [Content_Types].xml" {
		t.Fatalf("Expected missing [Content_Types].xml error; got: %v", err)
	}
}