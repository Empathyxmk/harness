package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

func DocsDecorator(fn func() string) func() string {
	return func() string {
		doc := fn()
		// Simulate printing docstring
		println(doc)
		return doc
	}
}

func TestDocsDecoratorPrintsDocstring(t *testing.T) {
	// Capture stdout
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	example := DocsDecorator(func() string {
		return "sample docstring for test"
	})

	result := example()
	w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	io.Copy(&buf, r)

	out := buf.String()
	if !strings.Contains(out, "sample docstring for test") {
		t.Errorf("Expected docstring to be printed, got: %v", out)
	}
	if result != "sample docstring for test" {
		t.Errorf("Expected decorator to return docstring, got: %v", result)
	}
}