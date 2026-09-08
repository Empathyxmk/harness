package public_tests

import (
	"bytes"
	"testing"
	pdfredactor "pdfredactor"
)

func TestPublicRedactorError_InvalidFilterTypeError(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	// Passing a non-string (int) pattern to simulate error
	options.ContentFilters = []pdfredactor.ContentFilter{
		{ Pattern: 12345 },
	}
	in := []byte("")
	out := &bytes.Buffer{}
	err := pdfredactor.RedactorWithStreams(options, in, out)
	if err == nil {
		t.Errorf("expected error on invalid filter type but got nil")
	}
}

func TestPublicRedactorError_InvalidOutputStream(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{}
	in := []byte("%PDF-1.3")
	// nil output stream
	err := pdfredactor.RedactorWithStreams(options, in, nil)
	if err == nil {
		t.Errorf("expected error on nil output stream but got nil")
	}
}