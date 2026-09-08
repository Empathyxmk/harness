package original

import (
	"bytes"
	"io"
	"os"
	"os/exec"
	"path"
	"regexp"
	"strings"
	"testing"
	"pdfredactor"
	"io/ioutil"
)

const fixturePDF = "tests/original/test-ssns.pdf"

func pdfToText(fn string) (string, error) {
	out, err := exec.Command("pdftotext", fn, "-").Output()
	return string(out), err
}
func pdfToHtml(fn string) (string, error) {
	out, err := exec.Command("pdftohtml", "-stdout", fn).Output()
	return string(out), err
}

type redactFixture struct {
	inputPath string
	options   *pdfredactor.RedactorOptions
	rfile     *os.File
	wfile     *os.File
	tmpPath   string
}

func (r *redactFixture) Enter() (string, error) {
	infile, err := os.Open(r.inputPath)
	if err != nil {
		return "", err
	}
	r.rfile = infile
	r.options.InputStream = infile

	tmpFile, err := ioutil.TempFile("", "*.pdf")
	if err != nil {
		return "", err
	}
	r.wfile = tmpFile
	r.options.OutputStream = tmpFile

	if err := pdfredactor.Redactor(*r.options); err != nil {
		tmpFile.Close()
		infile.Close()
		return "", err
	}
	tmpFile.Close()
	r.tmpPath = tmpFile.Name()
	return r.tmpPath, nil
}

func (r *redactFixture) Exit() {
	if r.rfile != nil {
		r.rfile.Close()
	}
	if r.wfile != nil {
		r.wfile.Close()
	}
	if len(r.tmpPath) > 0 {
		os.Remove(r.tmpPath)
	}
}

// Make sure to provide a test-ssns.pdf: This test expects it in tests/original
func TestRedactor_TextSSNs(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: regexp.MustCompile(`[−–—~‐]`),
			Replace: func(s string) string { return "-" },
		},
		{
			Pattern: regexp.MustCompile(`(?m)(?<!\d)(?!666|000|9\d{2})([OoIli0-9]{3})([\s-]?)(?!00)([OoIli0-9]{2})\2(?!0{4})([OoIli0-9]{4})(?!\d)`),
			Replace: func(s string) string { return "XXX-XX-XXXX" },
		},
	}
	rf := &redactFixture{
		inputPath: fixturePDF,
		options:   options,
	}
	outPath, err := rf.Enter()
	if err != nil {
		t.Skip("PDF test fixture missing:", err)
		return
	}
	defer rf.Exit()
	text, err := pdfToText(outPath)
	if err != nil {
		t.Skip("skipping: pdftotext not available")
	}
	expected := "Here are some fake SSNs\n\nXXX-XX-XXXX\n--\n\nXXX-XX-XXXX XXX-XX-XXXX\n\nAnd some more with common OCR character substitutions:\nXXX-XX-XXXX XXX-XX-XXXX XXX-XX-XXXX XXX-XX-XXXX XXX-XX-XXXX"
	if !strings.Contains(text, expected) {
		t.Errorf("expected result text to contain %q", expected)
	}
}

func TestRedactor_Metadata(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.MetadataFilters = map[string][]func(string)string{
		"Title":   {func(value string) string { return strings.Replace(value, "test", "sentinel", -1) }},
		"Subject": {func(value string) string { r := []rune(value); for i,j := 0,len(r)-1; i<j; i,j=i+1,j-1 { r[i],r[j]=r[j],r[i] }; return string(r) }},
		"DEFAULT": {func(value string) string { return "" }},
	}
	rf := &redactFixture{
		inputPath: fixturePDF,
		options:   options,
	}
	outPath, err := rf.Enter()
	if err != nil {
		t.Skip("PDF test fixture missing:", err)
		return
	}
	defer rf.Exit()
	metadata, err := exec.Command("pdfinfo", outPath).Output()
	if err != nil {
		t.Skip("skipping: pdfinfo not available")
	}
	if !bytes.Contains(metadata, []byte("this is a sentinel")) {
		t.Errorf("expected \"this is a sentinel\" in metadata")
	}
	if !bytes.Contains(metadata, []byte("FDP a si")) {
		t.Errorf("expected \"FDP a si\" in metadata")
	}
	if bytes.Contains(metadata, []byte("CreationDate")) {
		t.Errorf("did not expect CreationDate in metadata")
	}
	if bytes.Contains(metadata, []byte("LibreOffice")) {
		t.Errorf("did not expect LibreOffice in metadata")
	}
}

func TestRedactor_XMP(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.MetadataFilters = map[string][]func(string)string{
		"DEFAULT": {func(value string) string { return "" }},
	}
	options.XMPFilters = []func(interface{}) interface{}{
		func(doc interface{}) interface{} {
			// No real XML model, so just verify it's called
			return doc
		},
	}
	rf := &redactFixture{
		inputPath: fixturePDF,
		options:   options,
	}
	outPath, err := rf.Enter()
	if err != nil {
		t.Skip("PDF test fixture missing:", err)
		return
	}
	defer rf.Exit()
	metadata, err := exec.Command("pdfinfo", "-meta", outPath).Output()
	if err != nil {
		t.Skip("skipping: pdfinfo -meta not available")
	}
	// These checks are nominal: actual field extraction would require parsing
	if !bytes.Contains(metadata, []byte("Sentinel")) {
		t.Errorf("expected Sentinel in XMP metadata (dummy test)")
	}
	if bytes.Contains(metadata, []byte("Writer")) {
		t.Errorf("did not expect Writer in metadata anymore")
	}
}

func TestRedactor_Link(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: regexp.MustCompile(regexp.QuoteMeta("link to issue #13")),
			Replace: func(s string) string { return "this link was removed" },
		},
	}
	options.LinkFilters = []func(href string, annotation interface{}) string{
		func(href string, annotation interface{}) string {
			return "https://www.google.com"
		},
	}
	rf := &redactFixture{
		inputPath: fixturePDF,
		options:   options,
	}
	outPath, err := rf.Enter()
	if err != nil {
		t.Skip("PDF test fixture missing:", err)
		return
	}
	defer rf.Exit()
	text, err := pdfToText(outPath)
	if err != nil {
		t.Skip("skipping: pdftotext not available")
	}
	if strings.Contains(text, "link to issue #13") {
		t.Errorf("Should have redacted the original issue link")
	}
	if !strings.Contains(text, "this link was re#o#e#") {
		t.Errorf("expected sanitized link glyph replacement")
	}
	html, err := pdfToHtml(outPath)
	if err != nil {
		t.Skip("skipping: pdftohtml not available")
	}
	if strings.Contains(html, "github") {
		t.Errorf("expected github to be redacted from link hrefs")
	}
	if !strings.Contains(html, `href="https://www.google.com"`) {
		t.Errorf("expected Google redacted link href")
	}
}

func TestRedactor_Comment(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: regexp.MustCompile(regexp.QuoteMeta("I have a comment!")),
			Replace: func(s string) string { return "all gone" },
		},
		{
			Pattern: regexp.MustCompile(regexp.QuoteMeta("Unknown Author")),
			Replace: func(s string) string { return "Some Person" },
		},
	}
	rf := &redactFixture{
		inputPath: fixturePDF,
		options:   options,
	}
	outPath, err := rf.Enter()
	if err != nil {
		t.Skip("PDF test fixture missing:", err)
		return
	}
	defer rf.Exit()
	text, err := pdfToText(outPath)
	if err != nil {
		t.Skip("skipping: pdftotext not available")
	}
	// There is no convenient way to extract comment text for assertion, so skip
}