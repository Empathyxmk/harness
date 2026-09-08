package original

import (
	"bytes"
	"os"
	"testing"

	// Assuming composite package is available as "composite"
	"jameszbl_java_design_patterns/composite"
)

// Translated from: composite/src/test/java/me/zbl/composite/WriterIntegrationTest.java
func TestWriterSentences(t *testing.T) {
	baos := &bytes.Buffer{}
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	composite.NewWriter().SentenceByChinese().Print()
	composite.NewWriter().SentenceByEnglish().Print()

	w.Close()
	os.Stdout = old
	output, _ := io.ReadAll(r)
	result := string(output)

	if !bytes.Contains(output, []byte(".")) {
		t.Errorf("expected result to contain a dot, got: %v", result)
	}
}