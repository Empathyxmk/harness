package public_tests

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
	"jameszbl_java_design_patterns/composite"
)

func TestWriterSentencesPublic(t *testing.T) {
	baos := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	old := os.Stdout
	os.Stdout = w
	composite.NewWriter().SentenceByEnglish().Print()
	w.Close()
	os.Stdout = old
	result, _ := io.ReadAll(r)
	output := string(result)
	if !strings.Contains(output, "student") {
		t.Errorf("expected output to contain 'student', got: %s", output)
	}
	if !strings.Contains(output, "from") {
		t.Errorf("expected output to contain 'from', got: %s", output)
	}
}