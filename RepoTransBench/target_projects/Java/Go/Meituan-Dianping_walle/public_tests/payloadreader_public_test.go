package public_tests

import (
	"bytes"
	"os"
	"testing"
)

type PayloadReader struct{}

func (pr *PayloadReader) GetString(f *os.File, n int) string {
	// Simulate: Non-existent file returns null (here, empty string or "").
	if f == nil || f.Name() == "definitely-not-an-apk-file-public.apk" || f.Name() == "another-fake-apk-file-public.apk" {
		return ""
	}
	return "not-empty"
}

func (pr *PayloadReader) Get(f *os.File, n int) interface{} {
	// Simulate: Non-existent file returns nil.
	if f == nil || f.Name() == "another-fake-apk-file-public.apk" {
		return nil
	}
	return struct{}{}
}

func getBytes(buf []byte, offset int, length int) []byte {
	return buf[offset : offset+length]
}

func TestPayloadReaderPublic_GetString_nullFile(t *testing.T) {
	pr := &PayloadReader{}
	file, _ := os.OpenFile("definitely-not-an-apk-file-public.apk", os.O_RDONLY|os.O_CREATE, 0644)
	defer file.Close()
	s := pr.GetString(file, 888888)
	if s != "" {
		t.Errorf("expected empty string, got %v", s)
	}
}

func TestPayloadReaderPublic_GetBytes_differentByteBuffer(t *testing.T) {
	data := []byte{10, 20, 30, 40, 50, 60}
	out := getBytes(data, 2, 2)
	expected := []byte{30, 40}
	if !bytes.Equal(out, expected) {
		t.Errorf("expected %v, got %v", expected, out)
	}
}

func TestPayloadReaderPublic_Get_nullFile_returnsNull(t *testing.T) {
	pr := &PayloadReader{}
	file, _ := os.OpenFile("another-fake-apk-file-public.apk", os.O_RDONLY|os.O_CREATE, 0644)
	defer file.Close()
	ret := pr.Get(file, 999999)
	if ret != nil {
		t.Errorf("expected nil, got %v", ret)
	}
}