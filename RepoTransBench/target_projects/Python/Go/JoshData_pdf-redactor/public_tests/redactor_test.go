package public_tests

import (
	"bytes"
	"testing"
	pdfredactor "pdfredactor"
)

func TestPublicRedactor_BasicRedaction(t *testing.T) {
	pdfIn := []byte("%PDF-1.4\n% Public test: secret12345 replaced\nxyz 654-32-1987 zyx\n%%EOF")
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: `\b654-32-1987\b`,
			Replace: func(str string) string { return "[REDACTED-ID]" },
		},
	}
	out := &bytes.Buffer{}
	err := pdfredactor.RedactorWithStreams(options, pdfIn, out)
	if err != nil {
		t.Fatalf("error running redactor: %v", err)
	}
	if !bytes.Contains(out.Bytes(), []byte("[REDACTED-ID]")) {
		t.Errorf("expected output to contain [REDACTED-ID]")
	}
}

func TestPublicRedactor_UnicodeFilter(t *testing.T) {
	pdfIn := []byte("%PDF-1.4\nUnusual symbol: §\nID 88-99-7766\n%%EOF")
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: `\b88-99-7766\b`,
			Replace: func(str string) string { return "<REMOVED>" },
		},
	}
	out := &bytes.Buffer{}
	err := pdfredactor.RedactorWithStreams(options, pdfIn, out)
	if err != nil {
		t.Fatalf("error running redactor: %v", err)
	}
	if !bytes.Contains(out.Bytes(), []byte("<REMOVED>")) {
		t.Errorf("expected output to contain <REMOVED>")
	}
}

func TestPublicRedactor_MultilineFilter(t *testing.T) {
	pdfIn := []byte("%PDF-1.4\nFirstLine\nID: 222-33-4444\nSecondLine\n%%EOF")
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: "222-33-4444",
			Replace: func(str string) string { return "*****" },
		},
	}
	out := &bytes.Buffer{}
	err := pdfredactor.RedactorWithStreams(options, pdfIn, out)
	if err != nil {
		t.Fatalf("error running redactor: %v", err)
	}
	if !bytes.Contains(out.Bytes(), []byte("*****")) {
		t.Errorf("expected output to contain *****")
	}
}