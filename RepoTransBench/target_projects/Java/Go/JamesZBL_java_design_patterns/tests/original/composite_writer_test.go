package original

import (
	"bytes"
	"os"
	"strings"
	"testing"

	"jameszbl_java_design_patterns/composite"
)

// Translated from: composite/src/test/java/me/zbl/composite/WriterTest.java

var realStdOut = os.Stdout

func setUpStdOut() (*bytes.Buffer, func()) {
	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	os.Stdout = w
	return buf, func() {
		w.Close()
		os.Stdout = realStdOut
	}
}

func TestWriterSentenceByChinese(t *testing.T) {
	writer := composite.NewWriter()
	testWriterCn(t, writer.SentenceByChinese(), "我是来自北京的小明。")
}

func TestWriterSentenceByEnglish(t *testing.T) {
	writer := composite.NewWriter()
	testWriter(t, writer.SentenceByEnglish(), "I am a student from London.")
}

func testWriter(t *testing.T, givenComposite composite.CharacterComposite, expectedString string) {
	words := strings.Fields(strings.TrimSpace(expectedString))
	if givenComposite == nil {
		t.Fatal("givenComposite must not be nil")
	}
	if got := givenComposite.Count(); got != len(words) {
		t.Errorf("expected count %d, got %d", len(words), got)
	}

	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	os.Stdout = w

	givenComposite.Print()
	w.Close()
	os.Stdout = realStdOut

	result, _ := io.ReadAll(r)
	gotStr := strings.TrimSpace(string(result))
	if expectedString != gotStr {
		t.Errorf("expected '%s', got '%s'", expectedString, gotStr)
	}
}

func testWriterCn(t *testing.T, givenComposite composite.CharacterComposite, expectedString string) {
	if givenComposite == nil {
		t.Fatal("givenComposite must not be nil")
	}
	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	os.Stdout = w

	givenComposite.Print()
	w.Close()
	os.Stdout = realStdOut
	result, _ := io.ReadAll(r)
	gotStr := strings.TrimSpace(string(result))
	if expectedString != gotStr {
		t.Errorf("expected '%s', got '%s'", expectedString, gotStr)
	}
}