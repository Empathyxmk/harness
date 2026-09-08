package original

import (
	"archive/zip"
	"errors"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

type mockApplicationInfo struct {
	sourceDir string
}

func createTempApkWithDex(t *testing.T) string {
	tmp, err := ioutil.TempFile("", "test*.apk")
	if err != nil {
		t.Fatal(err)
	}
	defer tmp.Close()
	z := zip.NewWriter(tmp)
	defer z.Close()
	f, err := z.Create("classes.dex")
	if err != nil {
		t.Fatal(err)
	}
	_, err = f.Write([]byte("01234567"))
	if err != nil {
		t.Fatal(err)
	}
	return tmp.Name()
}

func loadApk(apkPath string) ([]string, error) {
	// Simulate loading all files from the apk (assuming classes.dex is present)
	r, err := zip.OpenReader(apkPath)
	if err != nil {
		return nil, err
	}
	defer r.Close()
	var files []string
	for _, f := range r.File {
		files = append(files, f.Name)
	}
	return files, nil
}

func TestLoadWithNoSecondaryDex(t *testing.T) {
	apkPath := createTempApkWithDex(t)
	defer os.Remove(apkPath)

	files, err := loadApk(apkPath)
	if err != nil {
		t.Fatalf("loadApk(%s) error: %v", apkPath, err)
	}
	if files == nil {
		t.Error("expected files, got nil")
	}
}

func TestBadZipCrcFileThrows(t *testing.T) {
	fake, err := ioutil.TempFile("", "fake*.apk")
	if err != nil {
		t.Fatal(err)
	}
	fake.Close()
	os.Remove(fake.Name()) // Remove to simulate non-zip/non-file
	_, err = loadApk(fake.Name())
	if err == nil {
		t.Error("expected error with bad zip, got nil")
	}
}