package original

import (
	"bytes"
	"regexp"
	"testing"
	pdfredactor "pdfredactor"
)

type DummyPdf struct {
	Info struct {
		Title       string
		Author      string
		Producer    string
		Creator     string
		CreationDate string
	}
}

func dummyPdfReader(stream interface{}) *DummyPdf {
	d := &DummyPdf{}
	d.Info.Title = "title"
	d.Info.Author = "author"
	d.Info.Producer = "producer"
	d.Info.Creator = "creator"
	d.Info.CreationDate = "date"
	return d
}

func dummyPdfWriter(doc *DummyPdf, stream interface{}) {}

type DummyOptions struct {
	pdfredactor.RedactorOptions
}

func TestRedactorFilterMechanics_MetadataUpdate(t *testing.T) {
	// Only test that the metadata_filters logic executes.
	opts := pdfredactor.NewRedactorOptions()
	opts.InputStream = bytes.NewBuffer([]byte("%PDF-1.4 mock pdf"))
	opts.OutputStream = &bytes.Buffer{}
	opts.MetadataFilters = map[string][]func(string)string{
		"Title":   {func(v string) string { return "UPPER" }},
		"DEFAULT": {func(v string) string { return "" }},
	}
	// PdfWriter/Reader, update_metadata, update_xmp_metadata would be mocked in a real test suite
	_ = pdfredactor.Redactor(opts)
}

func TestRedactorFilterMechanics_ContentFilter(t *testing.T) {
	opts := pdfredactor.NewRedactorOptions()
	opts.InputStream = bytes.NewBuffer([]byte("%PDF-1.4..."))
	opts.OutputStream = &bytes.Buffer{}
	opts.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: regexp.MustCompile("foo"),
			Replace: func(s string) string { return "bar" },
		},
	}
	_ = pdfredactor.Redactor(opts)
}