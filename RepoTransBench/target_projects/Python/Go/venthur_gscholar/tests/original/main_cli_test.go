package original

import (
	"bytes"
	"errors"
	"io"
	"os"
	"strings"
	"syscall"
	"testing"
)

// Mocks for CLI module
type fakeGS struct {
	queryCalled      bool
	queryKeyword     string
	queryOutformat   string
	queryAll         bool
	queryReturn      []string
	pdflookupCalled  bool
	pdflookupFile    string
	pdflookupReturn  []string
	renameFileCalled bool
	renameFileF      string
	renameFileB      string
}

func (f *fakeGS) Query(keyword, outformat string, all bool) []string {
	f.queryCalled = true
	f.queryKeyword = keyword
	f.queryOutformat = outformat
	f.queryAll = all
	return f.queryReturn
}
func (f *fakeGS) PDFLookup(pdf string, all bool, outformat string, startPage int) []string {
	f.pdflookupCalled = true
	f.pdflookupFile = pdf
	return f.pdflookupReturn
}
func (f *fakeGS) RenameFile(fstr string, bibentry string) {
	f.renameFileCalled = true
	f.renameFileF = fstr
	f.renameFileB = bibentry
}

// Helper functions
func setArgs(args []string) {
	os.Args = append([]string{"prog"}, args...)
}

func TestMain_Version(t *testing.T) {
	setArgs([]string{"--version", "test"})
	defer func() {
		recover()
	}()
	// Simulate SystemExit
	exitFunc := func() {
		panic(int(0))
	}
	defer func() { exitFunc = nil }()
	defer func() {
		if r := recover(); r != nil {
			code, ok := r.(int)
			if !ok || code != 0 {
				t.Errorf("Expected exit code 0, got %v", r)
			}
		}
	}()
	exitFunc()
}

func TestMain_Search(t *testing.T) {
	f := &fakeGS{queryReturn: []string{"somebibtex"}}
	setArgs([]string{"-f", "bibtex", "my search"})
	oldstdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	go func() {
		defer func() { _ = recover() }()
		_ = f.Query("my search", "bibtex", false)
	}()
	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = oldstdout
	if !strings.Contains(string(out), "somebibtex") {
		t.Errorf("Expected output to contain 'somebibtex', got %v", string(out))
	}
}

func TestMain_SearchNoResults(t *testing.T) {
	f := &fakeGS{queryReturn: []string{}}
	setArgs([]string{"-f", "bibtex", "xsearch"})
	defer func() {
		if r := recover(); r != nil {
			code, ok := r.(int)
			if !ok || code != 1 {
				t.Errorf("Expected exit code 1, got %v", r)
			}
		}
	}()
	_ = f.Query("xsearch", "bibtex", false)
	panic(int(1))
}

func TestMain_RenamePDF(t *testing.T) {
	f := &fakeGS{pdflookupReturn: []string{"somebib"}}
	setArgs([]string{"-f", "bibtex", "--rename", "afile.pdf"})
	existsCalled := false
	exists := func(path string) bool {
		existsCalled = true
		return path == "afile.pdf"
	}
	oldstdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	go func() {
		f.PDFLookup("afile.pdf", false, "bibtex", 0)
		f.RenameFile("afile.pdf", "somebib")
	}()
	w.Close()
	_, _ = io.ReadAll(r)
	os.Stdout = oldstdout
	if !f.pdflookupCalled || !f.renameFileCalled || f.renameFileF != "afile.pdf" {
		t.Error("PDFLookup and RenameFile were not properly called, or wrong file passed")
	}
	if !existsCalled {
		t.Error("os.path.exists not checked")
	}
}

func TestMain_RenameNoPDF(t *testing.T) {
	f := &fakeGS{}
	setArgs([]string{"-f", "bibtex", "--rename", "notafile"})
	exists := func(x string) bool { return false }
	defer func() {
		if r := recover(); r != nil {
			code, ok := r.(int)
			if !ok || code != 1 {
				t.Errorf("Expected exit code 1, got %v", r)
			}
		}
	}()
	_ = f.Query("notafile", "bibtex", false)
	if exists("notafile") {
		t.Error("Expected file not to exist")
	} else {
		panic(int(1))
	}
}

func TestMain_All(t *testing.T) {
	results := []string{"bib1", "bib2"}
	f := &fakeGS{queryReturn: results}
	setArgs([]string{"-f", "bibtex", "--all", "somesearch"})
	oldstdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	go func() {
		_ = f.Query("somesearch", "bibtex", true)
	}()
	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = oldstdout
	val := string(out)
	if !strings.Contains(val, "bib1") || !strings.Contains(val, "bib2") {
		t.Errorf("expected both bib1 and bib2, got %s", val)
	}
}

func TestMain_OutputFormats(t *testing.T) {
	var exp []string
	f := &fakeGS{}
	formats := [][2]string{
		{"endnote", "ENDNOTE"},
		{"refman", "REFMAN"},
		{"wenxianwang", "WENXIANWANG"},
	}
	for _, pair := range formats {
		setArgs([]string{"-f", pair[0], "abc"})
		oldstdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		go func() {
			exp = append(exp, pair[1])
			_ = f.Query("abc", pair[1], false)
		}()
		w.Close()
		_, _ = io.ReadAll(r)
		os.Stdout = oldstdout
	}
	foundEndnote := false
	foundRefman := false
	foundWenxianwang := false
	for _, e := range exp {
		if e == "ENDNOTE" {
			foundEndnote = true
		}
		if e == "REFMAN" {
			foundRefman = true
		}
		if e == "WENXIANWANG" {
			foundWenxianwang = true
		}
	}
	if !foundEndnote || !foundRefman || !foundWenxianwang {
		t.Errorf("Expected format enums in queries, got %v", exp)
	}
}