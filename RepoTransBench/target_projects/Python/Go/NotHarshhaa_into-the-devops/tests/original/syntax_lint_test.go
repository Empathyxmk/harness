package original

import (
	"bytes"
	"context"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"not_harshhaa_into_the_devops/syntaxlint"
)

func TestCountDetails(t *testing.T) {
	t.Run("balanced", func(t *testing.T) {
		lines := [][]byte{
			[]byte("<details>\n"),
			[]byte("content\n"),
			[]byte("</details>\n"),
		}
		out := syntaxlint.CountDetails(lines)
		if !out {
			t.Errorf("expected true for balanced details, got false")
		}
	})
	t.Run("unbalanced more opens", func(t *testing.T) {
		lines := [][]byte{
			[]byte("<details>\n"),
			[]byte("stuff\n"),
		}
		if syntaxlint.CountDetails(lines) {
			t.Errorf("expected false for unbalanced details (more opens), got true")
		}
	})
	t.Run("unbalanced more closes", func(t *testing.T) {
		lines := [][]byte{
			[]byte("</details>\n"),
			[]byte("<details>\n"),
			[]byte("</details>\n"),
		}
		if syntaxlint.CountDetails(lines) {
			t.Errorf("expected false for unbalanced details (more closes), got true")
		}
	})
}

func TestCountSummary(t *testing.T) {
	t.Run("balanced summary", func(t *testing.T) {
		lines := [][]byte{
			[]byte("<summary>\n"),
			[]byte("foo\n"),
			[]byte("</summary>\n"),
		}
		if !syntaxlint.CountSummary(lines) {
			t.Errorf("expected true for balanced summary tags")
		}
	})
	t.Run("unbalanced summary open", func(t *testing.T) {
		lines := [][]byte{
			[]byte("<summary>\n"),
			[]byte("foo\n"),
		}
		if syntaxlint.CountSummary(lines) {
			t.Errorf("expected false for unbalanced summary")
		}
	})
	t.Run("unbalanced summary close", func(t *testing.T) {
		lines := [][]byte{
			[]byte("foo\n"),
			[]byte("</summary>\n"),
		}
		if syntaxlint.CountSummary(lines) {
			t.Errorf("expected false for unbalanced summary (close)")
		}
	})
}

func TestCheckDetailsTag(t *testing.T) {
	resetErrors := func() { syntaxlint.Errors = syntaxlint.Errors[:0] }

	t.Run("correct nesting", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<details>\n"),
			[]byte("text\n"),
			[]byte("</details>\n"),
		}
		syntaxlint.CheckDetailsTag(lines)
		if len(syntaxlint.Errors) != 0 {
			t.Errorf("expected no errors for correct nesting, got %v", syntaxlint.Errors)
		}
	})

	t.Run("missing closing", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<details>\n"),
			[]byte("<details>\n"),
		}
		syntaxlint.CheckDetailsTag(lines)
		found := false
		for _, err := range syntaxlint.Errors {
			if bytes.Contains([]byte(err), []byte("Missing closing detail")) {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error for missing closing detail, got %v", syntaxlint.Errors)
		}
	})

	t.Run("missing opening", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("</details>\n"),
		}
		syntaxlint.CheckDetailsTag(lines)
		found := false
		for _, err := range syntaxlint.Errors {
			if bytes.Contains([]byte(err), []byte("Missing opening detail")) {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error for missing opening detail, got %v", syntaxlint.Errors)
		}
	})

	t.Run("oneline detail", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<details>foo</details>\n"),
		}
		syntaxlint.CheckDetailsTag(lines)
		if len(syntaxlint.Errors) != 0 {
			t.Errorf("expected no errors for single-line detail")
		}
	})
}

func TestCheckSummaryTag(t *testing.T) {
	resetErrors := func() { syntaxlint.Errors = syntaxlint.Errors[:0] }

	t.Run("correct summary", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<summary>\n"),
			[]byte("text\n"),
			[]byte("</summary>\n"),
		}
		syntaxlint.CheckSummaryTag(lines)
		if len(syntaxlint.Errors) != 0 {
			t.Errorf("expected no errors for correct summary tag, got %v", syntaxlint.Errors)
		}
	})

	t.Run("missing closing", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<summary>\n"),
			[]byte("<summary>\n"),
		}
		syntaxlint.CheckSummaryTag(lines)
		found := false
		for _, err := range syntaxlint.Errors {
			if bytes.Contains([]byte(err), []byte("Missing closing summary")) {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error for missing closing summary, got %v", syntaxlint.Errors)
		}
	})

	t.Run("missing opening", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("</summary>\n"),
		}
		syntaxlint.CheckSummaryTag(lines)
		found := false
		for _, err := range syntaxlint.Errors {
			if bytes.Contains([]byte(err), []byte("Missing opening summary")) {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error for missing opening summary, got %v", syntaxlint.Errors)
		}
	})

	t.Run("oneline summary", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<summary>xyz</summary>\n"),
		}
		syntaxlint.CheckSummaryTag(lines)
		if len(syntaxlint.Errors) != 0 {
			t.Errorf("expected no errors for single-line summary")
		}
	})

	t.Run("nested open", func(t *testing.T) {
		resetErrors()
		lines := [][]byte{
			[]byte("<summary>\n"),
			[]byte("<summary>\n"),
		}
		syntaxlint.CheckSummaryTag(lines)
		found := false
		for _, err := range syntaxlint.Errors {
			if bytes.Contains([]byte(err), []byte("Missing closing summary ")) ||
				bytes.Contains([]byte(err), []byte("Missing closing summary tag")) {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error for nested open summary, got %v", syntaxlint.Errors)
		}
	})
}

func TestCheckMdFile(t *testing.T) {
	resetErrors := func() { syntaxlint.Errors = syntaxlint.Errors[:0] }
	var oldP string

	t.Run("valid file", func(t *testing.T) {
		resetErrors()
		f, err := ioutil.TempFile("", "good*.md")
		if err != nil {
			t.Fatalf("failed to create tempfile: %v", err)
		}
		defer os.Remove(f.Name())
		content := []byte("<details>\ntext\n<summary>\ntext\n</summary>\n</details>\n")
		if _, err := f.Write(content); err != nil {
			t.Fatalf("failed to write: %v", err)
		}
		f.Close()
		oldP = syntaxlint.P
		syntaxlint.P = f.Name()

		syntaxlint.CheckMdFile(f.Name())
		if len(syntaxlint.Errors) != 0 {
			t.Errorf("expected no errors in valid file, got %v", syntaxlint.Errors)
		}
		syntaxlint.P = oldP
	})

	t.Run("file with errors", func(t *testing.T) {
		resetErrors()
		f, err := ioutil.TempFile("", "bad*.md")
		if err != nil {
			t.Fatalf("failed to create tempfile: %v", err)
		}
		defer os.Remove(f.Name())
		content := []byte("<details>\nno close\n<summary>\nno close\n")
		if _, err := f.Write(content); err != nil {
			t.Fatalf("failed to write: %v", err)
		}
		f.Close()
		oldP = syntaxlint.P
		syntaxlint.P = f.Name()

		syntaxlint.Errors = []string{}
		syntaxlint.CheckMdFile(f.Name())
		if syntaxlint.Errors == nil {
			t.Errorf("expected error slice after file with errors")
		}
		syntaxlint.P = oldP
	})
}

func TestMainGuard(t *testing.T) {
	resetErrors := func() { syntaxlint.Errors = syntaxlint.Errors[:0] }

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	t.Run("main block - good", func(t *testing.T) {
		resetErrors()
		f, err := ioutil.TempFile("", "good2*.md")
		if err != nil {
			t.Fatalf("failed to create tempfile: %v", err)
		}
		defer os.Remove(f.Name())
		content := []byte("<details>\n<summary>\ntest\n</summary>\n</details>\n")
		if _, err := f.Write(content); err != nil {
			t.Fatalf("failed to write: %v", err)
		}
		f.Close()

		os.Args = []string{"syntax_lint.go", f.Name()}
		origP := syntaxlint.P
		syntaxlint.P = f.Name()

		exitCode := -99
		origExiter := syntaxlint.Exiter
		syntaxlint.Exiter = func(code int) { exitCode = code }
		syntaxlint.MainGuard()
		syntaxlint.Exiter = origExiter
		syntaxlint.P = origP
		if exitCode == 1 {
			t.Errorf("should not exit with 1 for good input")
		}
	})

	t.Run("main block - bad", func(t *testing.T) {
		resetErrors()
		f, err := ioutil.TempFile("", "bad2*.md")
		if err != nil {
			t.Fatalf("failed to create tempfile: %v", err)
		}
		defer os.Remove(f.Name())
		content := []byte("<details>\n")
		if _, err := f.Write(content); err != nil {
			t.Fatalf("failed to write: %v", err)
		}
		f.Close()

		os.Args = []string{"syntax_lint.go", f.Name()}
		origP := syntaxlint.P
		syntaxlint.P = f.Name()

		exitCode := -99
		origExiter := syntaxlint.Exiter
		syntaxlint.Exiter = func(code int) { exitCode = code }
		syntaxlint.MainGuard()
		syntaxlint.Exiter = origExiter
		syntaxlint.P = origP
		if exitCode != 1 {
			t.Errorf("should exit with 1 for bad input, got %d", exitCode)
		}
	})
}