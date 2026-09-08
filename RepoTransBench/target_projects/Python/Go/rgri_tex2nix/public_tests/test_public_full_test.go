// public_tests/test_public_full_test.go
package tex2nix

import (
	"testing"
)

func TestFullTex2NixPipeline(t *testing.T) {
	tex := `
\documentclass[10pt]{report}
\usepackage{pdfpages}
\usepackage{mhchem}
`
	r := Latex2Nix(tex)
	pdfpg, mhchem := false, false
	numPdfpg := 0
	for _, p := range r {
		if p == "pdfpages" {
			pdfpg = true
			numPdfpg++
		}
		if p == "mhchem" {
			mhchem = true
		}
	}
	if !pdfpg {
		t.Errorf("Expected pdfpages in %v", r)
	}
	if !mhchem {
		t.Errorf("Expected mhchem in %v", r)
	}
	if numPdfpg != 1 {
		t.Errorf("Expected pdfpages only once, got %d", numPdfpg)
	}
	docclass, err := DetectDocumentclass(tex)
	if err != nil {
		t.Fatalf("Expected docclass, got error: %v", err)
	}
	if docclass != "report" {
		t.Errorf("Expected documentclass 'report', got %q", docclass)
	}
}