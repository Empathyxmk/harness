package public_tests

import (
	"archive/zip"
	"hash/crc32"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func createPublicTestZip(t *testing.T) string {
	tmpfile, err := ioutil.TempFile("", "ZipUtilPublicTest*.zip")
	if err != nil {
		t.Fatal(err)
	}
	defer tmpfile.Close()
	z := zip.NewWriter(tmpfile)
	defer z.Close()

	w1, err := z.Create("file1.txt")
	if err != nil {
		t.Fatal(err)
	}
	_, err = w1.Write([]byte("hello"))
	if err != nil {
		t.Fatal(err)
	}

	w2, err := z.Create("file2.txt")
	if err != nil {
		t.Fatal(err)
	}
	_, err = w2.Write([]byte("world"))
	if err != nil {
		t.Fatal(err)
	}
	return tmpfile.Name()
}

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

func TestCrcDoNotCrashPublic(t *testing.T) {
	path := createPublicTestZip(t)
	defer os.Remove(path)
	crc, err := getZipCrc(path)
	if err != nil {
		t.Fatalf("getZipCrc failed: %v", err)
	}
	if crc <= 0 {
		t.Errorf("crc is not positive: %d", crc)
	}
}

func TestCrcRangePublic(t *testing.T) {
	path := createPublicTestZip(t)
	defer os.Remove(path)
	r, err := zip.OpenReader(path)
	if err != nil {
		t.Fatal(err)
	}
	defer r.Close()
	expectedCount := len(r.File)
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
		t.Errorf("zip entry count mismatch: got %d want %d", count, expectedCount)
	}
}

func TestCrcValuePublic(t *testing.T) {
	path := createPublicTestZip(t)
	defer os.Remove(path)
	r, err := zip.OpenReader(path)
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
		rc.Close()
		if err != nil {
			t.Fatal(err)
		}
		crc := crc32.ChecksumIEEE(buf)
		if crc != f.CRC32 {
			t.Errorf("Expected CRC32 %v, got %v", f.CRC32, crc)
		}
	}
}

func TestInvalidCrcValuePublic(t *testing.T) {
	path := createPublicTestZip(t)
	defer os.Remove(path)
	r, err := zip.OpenReader(path)
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
		rc.Close()
		if err != nil {
			t.Fatal(err)
		}
		corrupted := append(buf, []byte("extra")...)
		crc := crc32.ChecksumIEEE(corrupted)
		if crc == f.CRC32 {
			t.Errorf("Corrupted buffer should not match original CRC32 %v", f.CRC32)
		}
	}
}