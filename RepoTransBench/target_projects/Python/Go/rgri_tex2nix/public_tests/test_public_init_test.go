// public_tests/test_public_init_test.go
package tex2nix

import (
	"os"
	"reflect"
	"strings"
	"testing"
)

func TestVersionSemver(t *testing.T) {
	ver := Version
	parts := strings.Split(ver, ".")
	if len(parts) != 3 {
		t.Errorf("Version should have three parts, got: %v", parts)
	}
}

func TestMainEntryReturnsNone(t *testing.T) {
	// Simulate the logic: when Main exists and is called, returns nil/void
	// Here, Main is a function that does nothing and returns nothing
	defer func(orig map[string]struct{}) { GetNixPackages = func() map[string]struct{} { return orig } }(GetNixPackages())
	GetNixPackages = func() map[string]struct{} {
		return map[string]struct{}{
			"standalone":    {},
			"publicpackage": {},
			"fancyhdr":      {},
			"longtable":     {},
			"pgfplots":      {},
			"subcaption":    {},
			"caption":       {},
			"blindtext":     {},
			"geometry":      {},
			"color":         {},
			"todonotes":     {},
			"colortbl":      {},
			"memoir":        {},
			"zref":          {},
			"moreverb":      {},
		}
	}
	tmpdir := t.TempDir()
	cwd, _ := os.Getwd()
	defer os.Chdir(cwd)
	os.Chdir(tmpdir)
	texFile := tmpdir + "/dummy.tex"
	os.WriteFile(texFile, []byte(`\documentclass{test}`), 0644)
	Main()
	// If we get here, Main did not panic or fail (has no return).
}

func TestLatex2NixExampleUsage(t *testing.T) {
	input := `
\documentclass{scrreprt}
\usepackage{fancyhdr}
\usepackage{longtable}
\begin{document}
LaTeX public sample!
\end{document}`
	result := Latex2Nix(input)
	if len(result) == 0 {
		t.Fatalf("Latex2Nix result must not be empty for given LaTeX")
	}
	found := make(map[string]bool)
	for _, p := range result {
		found[p] = true
	}
	if !found["fancyhdr"] {
		t.Errorf("Should find fancyhdr in: %v", result)
	}
	if !found["longtable"] {
		t.Errorf("Should find longtable in: %v", result)
	}
	if found["geometry"] {
		t.Errorf("Should not find geometry in: %v", result)
	}
}

func TestLatex2NixHandlesEmpty(t *testing.T) {
	r := Latex2Nix("")
	if len(r) != 0 {
		t.Errorf("Expected empty result, got: %v", r)
	}
}

func TestLatex2NixNoDuplicates(t *testing.T) {
	input := `
\usepackage{todonotes}
\usepackage{todonotes}
\usepackage{colortbl}`
	r := Latex2Nix(input)
	counts := map[string]int{}
	for _, p := range r {
		counts[p]++
	}
	if counts["todonotes"] != 1 {
		t.Errorf("Expected 1 occurrence of 'todonotes', got %d", counts["todonotes"])
	}
	if counts["colortbl"] != 1 {
		t.Errorf("Expected 1 occurrence of 'colortbl', got %d", counts["colortbl"])
	}
}

func TestLatex2NixCustomPackage(t *testing.T) {
	input := `
\documentclass{standalone}
\usepackage{publicpackage}
\begin{document}
Public
\end{document}`
	r := Latex2Nix(input)
	found := false
	for _, p := range r {
		if p == "publicpackage" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Expected 'publicpackage' in: %v", r)
	}
}

func TestLatex2NixMultilineUsepackage(t *testing.T) {
	input := `
\usepackage{pgfplots,
subcaption,
caption}
`
	r := Latex2Nix(input)
	for _, p := range []string{"pgfplots", "subcaption", "caption"} {
		if !contains(r, p) {
			t.Errorf("Expected %s in: %v", p, r)
		}
	}
}

func TestLatex2NixWithCommentLines(t *testing.T) {
	input := `
% Just a comment line
\usepackage{blindtext}
% trailing comment
`
	r := Latex2Nix(input)
	if !contains(r, "blindtext") {
		t.Errorf("Expected 'blindtext' in: %v", r)
	}
}

func TestLatex2NixOptionalArg(t *testing.T) {
	input := `
\usepackage[top=2cm]{geometry}
\usepackage[usenames]{color}
`
	r := Latex2Nix(input)
	if !contains(r, "geometry") {
		t.Errorf("Expected 'geometry' in %v", r)
	}
	if !contains(r, "color") {
		t.Errorf("Expected 'color' in %v", r)
	}
}

func TestLatex2NixIgnoresUnrelatedLines(t *testing.T) {
	input := `
123 random text line
\date{}
`
	r := Latex2Nix(input)
	if len(r) != 0 {
		t.Errorf("Expected empty, got: %v", r)
	}
}

func TestDetectDocumentclass(t *testing.T) {
	input := `
\documentclass{memoir}
\usepackage{zref}`
	class, err := DetectDocumentclass(input)
	if err != nil {
		t.Fatalf("DetectDocumentclass error: %v", err)
	}
	if class != "memoir" {
		t.Errorf("Expected memoir, got: %v", class)
	}
}

func TestDetectDocumentclassNone(t *testing.T) {
	input := `
% no docclass here
\usepackage{moreverb}`
	class, err := DetectDocumentclass(input)
	if err == nil {
		t.Errorf("Expected error for missing documentclass, got: %v", class)
	}
}

func contains(r []string, s string) bool {
	for _, x := range r {
		if x == s {
			return true
		}
	}
	return false
}