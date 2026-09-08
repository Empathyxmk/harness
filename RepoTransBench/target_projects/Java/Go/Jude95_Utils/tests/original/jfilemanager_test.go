package original

import (
	"encoding/gob"
	"io"
	"os"
	"path/filepath"
	"testing"
)

// DIR mapping (simulate Java Enum)
type Dir int

const (
	TEST Dir = iota
)

// JFileManager singleton mock
type JFileManager struct {
	baseDir string
}

func getInstance() *JFileManager {
	tmp := os.TempDir()
	path := filepath.Join(tmp, "jfilemanager_go_test")
	_ = os.MkdirAll(path, 0755)
	return &JFileManager{baseDir: path}
}

func (mgr *JFileManager) getFolder(_ Dir) *JFolder {
	return &JFolder{dir: mgr.baseDir}
}

func (mgr *JFileManager) clearAllData() {
	entries, _ := os.ReadDir(mgr.baseDir)
	for _, entry := range entries {
		_ = os.RemoveAll(filepath.Join(mgr.baseDir, entry.Name()))
	}
}

// JFolder represents a test folder under baseDir
type JFolder struct {
	dir string
}

func (f *JFolder) getFile() *os.File {
	file, _ := os.Open(f.dir)
	return file
}

func (f *JFolder) writeStringToFile(data, fname string) error {
	filePath := filepath.Join(f.dir, fname)
	return os.WriteFile(filePath, []byte(data), 0644)
}

func (f *JFolder) readStringFromFile(fname string) string {
	filePath := filepath.Join(f.dir, fname)
	b, err := os.ReadFile(filePath)
	if err != nil {
		return ""
	}
	return string(b)
}

func (f *JFolder) writeObjectToFile(obj interface{}, fname string) error {
	filePath := filepath.Join(f.dir, fname)
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()
	enc := gob.NewEncoder(file)
	return enc.Encode(obj)
}

func (f *JFolder) readObjectFromFile(fname string, out interface{}) error {
	filePath := filepath.Join(f.dir, fname)
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()
	dec := gob.NewDecoder(file)
	return dec.Decode(out)
}

func (f *JFolder) deleteChild(fname string) error {
	return os.Remove(filepath.Join(f.dir, fname))
}

func (f *JFolder) listChildFile() ([]string, error) {
	entries, err := os.ReadDir(f.dir)
	if err != nil {
		return nil, err
	}
	files := []string{}
	for _, e := range entries {
		files = append(files, e.Name())
	}
	return files, nil
}

func (f *JFolder) getChildFile(fname string) string {
	return filepath.Join(f.dir, fname)
}

// Test Object
type TestObj struct {
	X int
}

// ---------- TESTS ------------

func TestInitAndGetFolder(t *testing.T) {
	mgr := getInstance()
	folder := mgr.getFolder(TEST)
	if folder == nil {
		t.Fatal("Expected folder non-nil")
	}
	info, err := os.Stat(folder.dir)
	if err != nil {
		t.Fatalf("Folder doesn't exist: %v", err)
	}
	if !info.IsDir() {
		t.Error("Expected a directory")
	}
}

func TestWriteAndReadString(t *testing.T) {
	mgr := getInstance()
	folder := mgr.getFolder(TEST)
	err := folder.writeStringToFile("hello world", "string.txt")
	if err != nil {
		t.Fatalf("Failed to write string: %v", err)
	}
	read := folder.readStringFromFile("string.txt")
	if read != "hello world" {
		t.Errorf("String read does not match: %v", read)
	}
	// Non-existent file returns ""
	if folder.readStringFromFile("not_exist.txt") != "" {
		t.Error("Expected empty result on missing file")
	}
}

func TestWriteAndReadObject(t *testing.T) {
	mgr := getInstance()
	folder := mgr.getFolder(TEST)
	// Register type for gob
	gob.Register(TestObj{})
	obj := TestObj{X: 1234}
	if err := folder.writeObjectToFile(obj, "obj.bin"); err != nil {
		t.Fatalf("WriteObject failed: %v", err)
	}
	var read TestObj
	if err := folder.readObjectFromFile("obj.bin", &read); err != nil {
		t.Fatalf("readObjectFromFile failed: %v", err)
	}
	if read.X != 1234 {
		t.Errorf("Object value mismatch: %d", read.X)
	}
	_ = folder.deleteChild("obj.bin")
	err := folder.readObjectFromFile("obj.bin", &read)
	if err == nil || err == io.EOF { // should fail since file is deleted
		t.Errorf("Expected error after deleting file, got none")
	}
}

func TestListAndDeleteChild(t *testing.T) {
	mgr := getInstance()
	folder := mgr.getFolder(TEST)
	_ = folder.writeStringToFile("data1", "f1.txt")
	_ = folder.writeStringToFile("data2", "f2.txt")
	files, err := folder.listChildFile()
	if err != nil || len(files) != 2 {
		t.Errorf("Expected 2 files, got: %v", files)
	}
	_ = folder.deleteChild("f1.txt")
	files, _ = folder.listChildFile()
	if len(files) != 1 {
		t.Errorf("Expected 1 file after delete, got: %d", len(files))
	}
}

func TestClearAllData(t *testing.T) {
	mgr := getInstance()
	folder := mgr.getFolder(TEST)
	_ = folder.writeStringToFile("t", "f.txt")
	child := folder.getChildFile("f.txt")
	info, err := os.Stat(child)
	if err != nil || info == nil {
		t.Fatalf("file f.txt should exist but not: %v", err)
	}
	mgr.clearAllData()
	_, err2 := os.Stat(child)
	if err2 == nil {
		t.Errorf("file should not exist after clearAllData")
	}
}