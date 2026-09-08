package original

import (
	"os"
	"testing"
)

// Simulate Storage struct
type Storage struct {
	dbDir string
}

func NewStorage(dbName string) *Storage {
	tmpdir := os.TempDir()
	return &Storage{dbDir: tmpdir + "/" + dbName + "_" + RandString(10)}
}

func (s *Storage) DbDir() string {
	return s.dbDir
}

func TestItShouldAllowToMakeTwoStorageWithOneDatabaseName(t *testing.T) {
	storage0 := NewStorage("postgres")
	if _, err := os.Stat(storage0.DbDir()); os.IsNotExist(err) {
		_ = os.MkdirAll(storage0.DbDir(), 0755)
	}
	if _, err := os.Stat(storage0.DbDir()); os.IsNotExist(err) {
		t.Error("storage0 dbDir does not exist")
	}

	storage1 := NewStorage("postgres")
	if _, err := os.Stat(storage1.DbDir()); os.IsNotExist(err) {
		_ = os.MkdirAll(storage1.DbDir(), 0755)
	}
	if _, err := os.Stat(storage1.DbDir()); os.IsNotExist(err) {
		t.Error("storage1 dbDir does not exist")
	}

	if storage0.DbDir() == storage1.DbDir() {
		t.Error("Each Storage instance should have a unique path")
	}
}