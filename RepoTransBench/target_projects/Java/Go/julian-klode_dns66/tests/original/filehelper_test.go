package original

import (
	"bytes"
	"errors"
	"io"
	"testing"
)

func TestOpenReadExistingFile(t *testing.T) {
	content := []byte("existing")
	r := bytes.NewReader(content)
	b := make([]byte, len(content))
	_, err := r.Read(b)
	if err != nil {
		t.Fatalf("failed to read: %v", err)
	}
	if string(b) != "existing" {
		t.Errorf("expected to read 'existing'")
	}
}

func TestOpenReadFallbackToAsset(t *testing.T) {
	content := []byte("asset")
	r := bytes.NewReader(content)
	b := make([]byte, len(content))
	_, err := r.Read(b)
	if err != nil {
		t.Fatalf("failed to read fallback asset: %v", err)
	}
	if string(b) != "asset" {
		t.Errorf("expected fallback read 'asset'")
	}
}

func TestOpenWrite(t *testing.T) {
	var buf bytes.Buffer
	_, err := buf.Write([]byte("test"))
	if err != nil {
		t.Errorf("error writing to buffer: %v", err)
	}
	if buf.String() != "test" {
		t.Errorf("expected written content 'test', got %q", buf.String())
	}
}

type fakeClosable struct {
	closed bool
	fail   bool
}

func (f *fakeClosable) Close() error {
	f.closed = true
	if f.fail {
		return errors.New("close error")
	}
	return nil
}

func TestCloseOrWarn_Closeable(t *testing.T) {
	closer := &fakeClosable{}
	_ = closer.Close()
	if !closer.closed {
		t.Error("expected closed=true after Close")
	}
}

func TestCloseOrWarn_CloseableWithError(t *testing.T) {
	closer := &fakeClosable{fail: true}
	err := closer.Close()
	if err == nil {
		t.Error("expected error from Close")
	}
}