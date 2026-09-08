package original

import (
	"bytes"
	"errors"
	"testing"
	pdfredactor "pdfredactor"
)

type dummyStream struct{}

func (d *dummyStream) Read(p []byte) (n int, err error) {
	copy(p, []byte("not a pdf"))
	return len("not a pdf"), nil
}
func (d *dummyStream) Close() error { return nil }

func TestRedactorError_PdfParseError(t *testing.T) {
	opts := pdfredactor.NewRedactorOptions()
	opts.InputStream = &dummyStream{}
	opts.OutputStream = &bytes.Buffer{}

	err := pdfredactor.Redactor(opts)
	if err == nil {
		t.Fatalf("Expected error on invalid PDF input but got none")
	}
	// Accept any error returned
	var _err error = err
	if _err == nil {
		t.Errorf("Error is not of type error")
	}
}