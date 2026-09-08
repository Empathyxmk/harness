package public_tests

import (
	"bytes"
	"testing"
	pdfredactor "pdfredactor"
)

func TestPublicRedactorFilters_FilterCallableReplacement(t *testing.T) {
	pdfIn := []byte("%PDF-1.4\nSSN 159-46-2879\n%%EOF")
	repl := func(val string) string { return "MASKED" }
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: `\d{3}-\d{2}-\d{4}`,
			Replace: repl,
		},
	}
	out := &bytes.Buffer{}
	err := pdfredactor.RedactorWithStreams(options, pdfIn, out)
	if err != nil {
		t.Fatalf("error running redactor: %v", err)
	}
	if !bytes.Contains(out.Bytes(), []byte("MASKED")) {
		t.Errorf("expected output to contain MASKED")
	}
}

func TestPublicRedactorFilters_FilterNonCallableReplacement(t *testing.T) {
	pdfIn := []byte("%PDF-1.4\nName: Angela Bailey\n%%EOF")
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: "Angela Bailey",
			Replace: func(_ string) string { return "AnonName" },
		},
	}
	out := &bytes.Buffer{}
	err := pdfredactor.RedactorWithStreams(options, pdfIn, out)
	if err != nil {
		t.Fatalf("error running redactor: %v", err)
	}
	if !bytes.Contains(out.Bytes(), []byte("AnonName")) {
		t.Errorf("expected output to contain AnonName")
	}
}