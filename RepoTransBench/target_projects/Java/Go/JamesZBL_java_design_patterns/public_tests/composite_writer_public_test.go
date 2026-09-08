package public_tests

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
	"jameszbl_java_design_patterns/composite"
)

func TestWriterSentenceByChinesePublic(t *testing.T) {
	writer := composite.NewWriter()
	testWriterCn(t, writer.SentenceByChinese(), "我是来自北京的小明。")
}

func TestWriterSentenceByEnglishPublic(t *testing.T) {
	writer := composite.NewWriter()
	testWriterTrimmed(t, writer.SentenceByEnglish(), "I am a student from London.")
}

// Test output with trimmed and lower case
func testWriterTrimmed(t *testing.T, givenComposite composite.CharacterComposite, expected string) {
	words := strings.Fields(strings.TrimSpace(expected))
	if givenComposite == nil {
		t.Error("givenComposite is nil")
	}
	if givenComposite.Count() != len(words) {
		t.Errorf("count: got %d, want %d", givenComposite.Count(), len(words))
	}

	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	old := os.Stdout
	os.Stdout = w

	givenComposite.Print()

	w.Close()
	os.Stdout = old
	result, _ := io.ReadAll(r)
	output := strings.TrimSpace(strings.ToLower(string(result)))
	want := strings.TrimSpace(strings.ToLower(expected))
	if !strings.HasSuffix(output, ".") {
		t.Errorf("output %q must end with '.'", output)
	}
	if output != want {
		t.Errorf("output %q != want %q", output, want)
	}
}

func testWriterCn(t *testing.T, givenComposite composite.CharacterComposite, expected string) {
	if givenComposite == nil {
		t.Error("givenComposite is nil")
	}
	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	old := os.Stdout
	os.Stdout = w
	givenComposite.Print()
	w.Close()
	os.Stdout = old
	result, _ := io.ReadAll(r)
	output := strings.TrimSpace(string(result))
	if !strings.Contains(output, "北京") {
		t.Errorf("output should contain 北京, got %q", output)
	}
	if !strings.HasSuffix(output, "。") {
		t.Errorf("output must end with '。', got %q", output)
	}
}