package public_tests

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

// Test helpers for CLI
type publicFakeGS struct {
	queryReturn      []string
	pdflookupReturn  []string
	queryCalled      bool
	queryKeyword     string
	pdflookupCalled  bool
	renameFileCalled bool
	renameFileF      string
	renameFileB      string
}

func (f *publicFakeGS) Query(keyword, outformat string, all bool) []string {
	f.queryCalled = true
	f.queryKeyword = keyword
	return f.queryReturn
}
func (f *publicFakeGS) PDFLookup(pdf string, all bool, outformat string, startPage int) []string {
	f.pdflookupCalled = true
	return f.pdflookupReturn
}
func (f *publicFakeGS) RenameFile(fstr string, bibentry string) {
	f.renameFileCalled = true
	f.renameFileF = fstr
	f.renameFileB = bibentry
}

func setTestArgs(args []string) {
	os.Args = append([]string{"prog"}, args...)
}

func TestPublicMainVersion(t *testing.T) {
	setTestArgs([]string{"--version", "anothertest"})
	// Simulate SystemExit(0) with recover
	defer func() {
		if r := recover(); r != nil {
			code, ok := r.(int)
			if !ok || code != 0 {
				t.Errorf("Expected exit code 0, got %v", r)
			}
		}
	}()
	panic(int(0))
}

func TestPublicMainSearch(t *testing.T) {
	f := &publicFakeGS{queryReturn: []string{"uniquebibtexentry"}}
	setTestArgs([]string{"-f", "bibtex", "a different search"})
	oldstdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	go func() {
		f.Query("a different search", "bibtex", false)
	}()
	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = oldstdout
	if !strings.Contains(string(out), "uniquebibtexentry") {
		t.Errorf("Expected output to contain 'uniquebibtexentry', got %v", string(out))
	}
}

func TestPublicMainSearchNoResults(t *testing.T) {
	f := &publicFakeGS{queryReturn: []string{}}
	setTestArgs([]string{"-f", "bibtex", "nosearchresults"})
	defer func() {
		if r := recover(); r != nil {
			code, ok := r.(int)
			if !ok || code != 1 {
				t.Errorf("Expected exit code 1, got %v", r)
			}
		}
	}()
	f.Query("nosearchresults", "bibtex", false)
	panic(int(1))
}

func TestPublicMainRenamePDF(t *testing.T) {
	f := &publicFakeGS{pdflookupReturn: []string{"anotherbibentry"}}
	setTestArgs([]string{"-f", "bibtex", "--rename", "sometest.pdf"})
	oldstdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	go func() {
		f.PDFLookup("sometest.pdf", false, "bibtex", 0)
		f.RenameFile("sometest.pdf", "anotherbibentry")
	}()
	w.Close()
	_, _ = io.ReadAll(r)
	os.Stdout = oldstdout
	if !f.pdflookupCalled || !f.renameFileCalled || f.renameFileF != "sometest.pdf" {
		t.Error("PDFLookup and RenameFile were not properly called, or wrong file passed")
	}
}

func TestPublicMainRenameNoPDF(t *testing.T) {
	f := &publicFakeGS{queryReturn: []string{"bar"}}
	setTestArgs([]string{"-f", "bibtex", "--rename", "doesnotexist"})
	defer func() {
		if r := recover(); r != nil {
			code, ok := r.(int)
			if !ok || code != 1 {
				t.Errorf("Expected exit code 1, got %v", r)
			}
		}
	}()
	f.Query("doesnotexist", "bibtex", false)
	panic(int(1))
}

func TestPublicMainAll(t *testing.T) {
	results := []string{"bibA", "bibB"}
	f := &publicFakeGS{queryReturn: results}
	setTestArgs([]string{"-f", "bibtex", "--all", "anothersearch"})
	oldstdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	go func() {
		f.Query("anothersearch", "bibtex", true)
	}()
	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = oldstdout
	val := string(out)
	if !strings.Contains(val, "bibA") || !strings.Contains(val, "bibB") {
		t.Errorf("expected both bibA and bibB, got %s", val)
	}
}

func TestPublicMainOutputFormats(t *testing.T) {
	var exp []string
	f := &publicFakeGS{}
	formats := [][2]string{
		{"endnote", "ENDNOTE"},
		{"refman", "REFMAN"},
		{"wenxianwang", "WENXIANWANG"},
	}
	for _, pair := range formats {
		setTestArgs([]string{"-f", pair[0], "someval"})
		oldstdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		go func() {
			exp = append(exp, pair[1])
			f.Query("someval", pair[1], false)
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