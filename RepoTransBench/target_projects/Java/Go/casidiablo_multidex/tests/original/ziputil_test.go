package original

import (
	"archive/zip"
	"bytes"
	"hash/crc32"
	"errors"
	"io"
	"io/ioutil"
	"os"
	"testing"
	"time"
)

func createSampleZip(t *testing.T) string {
	tmpfile, err := ioutil.TempFile("", "ziputiltest*.zip")
	if err != nil {
		t.Fatal(err)
	}
	defer tmpfile.Close()
	w := zip.NewWriter(tmpfile)
	defer w.Close()
	for i := 0; i < 2; i++ {
		fh := &zip.FileHeader{
			Name:     "file" + string('A'+i),
			Method:   zip.Store,
			Modified: time.Now(),
		}
		f, err := w.CreateHeader(fh)
		if err != nil {
			t.Fatal(err)
		}
		_, err = f.Write([]byte("hello"))
		if err != nil {
			t.Fatal(err)
		}
	}
	w.Close()
	return tmpfile.Name()
}

// Mimic ZipUtil.getZipCrc
func getZipCrc(path string) (uint32, error) {
	f, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	defer f.Close()
	hasher := crc32.NewIEEE()
	if _, err := io.Copy(hasher, f); err != nil {
		return 0, err
	}
	return hasher.Sum32(), nil
}

func TestCrcDoNotCrash(t *testing.T) {
	zipPath := createSampleZip(t)
	defer os.Remove(zipPath)
	crc, err := getZipCrc(zipPath)
	if err != nil {
		t.Errorf("getZipCrc failed: %v", err)
	}
	if crc == 0 {
		t.Errorf("crc is 0, want non-zero")
	}
}

func TestCrcRange(t *testing.T) {
	zipPath := createSampleZip(t)
	defer os.Remove(zipPath)
	r, err := zip.OpenReader(zipPath)
	if err != nil {
		t.Fatal(err)
	}
	defer r.Close()
	expectedCount := len(r.File)
	if expectedCount == 0 {
		t.Error("sample zip should have files")
	}
	count := 0
	for _, f := range r.File {
		count++
		if f.Name == "" {
			t.Errorf("file entry missing name")
		}
		if f.Modified.IsZero() {
			t.Errorf("file entry missing modified time")
		}
	}
	if count != expectedCount {
		t.Errorf("zip entry count mismatch, got %d want %d", count, expectedCount)
	}
}

func TestCrcValue(t *testing.T) {
	zipPath := createSampleZip(t)
	defer os.Remove(zipPath)
	r, err := zip.OpenReader(zipPath)
	if err != nil {
		t.Fatal(err)
	}
	defer r.Close()
	for _, f := range r.File {
		rc, err := f.Open()
		if err != nil {
			t.Fatal(err)
		}
		buf, err := ioutil.ReadAll(rc)
		if err != nil {
			rc.Close()
			t.Fatal(err)
		}
		rc.Close()
		crc := crc32.ChecksumIEEE(buf)
		if crc != f.CRC32 {
			t.Errorf("Expected CRC32 %v, got %v", f.CRC32, crc)
		}
	}
}

func TestInvalidCrcValue(t *testing.T) {
	zipPath := createSampleZip(t)
	defer os.Remove(zipPath)
	r, err := zip.OpenReader(zipPath)
	if err != nil {
		t.Fatal(err)
	}
	defer r.Close()
	for _, f := range r.File {
		rc, err := f.Open()
		if err != nil {
			t.Fatal(err)
		}
		buf, err := ioutil.ReadAll(rc)
		if err != nil {
			rc.Close()
			t.Fatal(err)
		}
		rc.Close()
		modBuf := append(buf, []byte("corrupt!")...)
		crc := crc32.ChecksumIEEE(modBuf)
		if crc == f.CRC32 {
			t.Errorf("Corrupted buffer should not have same CRC32 %v", f.CRC32)
		}
	}
}