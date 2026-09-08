package original

import (
	"os"
	"testing"

	"filemanager"
)

func removeIfExists(t *testing.T, filename string) {
	if filename == "" {
		return
	}
	if _, err := os.Stat(filename); err == nil {
		if err := os.Remove(filename); err != nil {
			t.Fatalf("Failed to clean up file %s: %v", filename, err)
		}
	}
}

func TestFileManagerTestSuite(t *testing.T) {
	fm := &filemanager.FileManager{}
	testFile := "testfile.txt"
	copiedFile := "copiedfile.txt"
	var nullFile string // "" is the closest analog to Java null

	// Clean up before & after each test case
	cleanup := func() {
		removeIfExists(t, testFile)
		removeIfExists(t, copiedFile)
		removeIfExists(t, "dummy.txt")
	}

	t.Run("testFileExists_false", func(t *testing.T) {
		defer cleanup()
		if fm.FileExists("notreallypresent.txt") {
			t.Errorf("Expected file to not exist")
		}
	})

	t.Run("testFileExists_true", func(t *testing.T) {
		defer cleanup()
		f, err := os.Create(testFile)
		if err != nil {
			t.Fatalf("Could not create file: %v", err)
		}
		f.Close()
		if !fm.FileExists(testFile) {
			t.Errorf("Expected file to exist")
		}
	})

	t.Run("testFileExists_null", func(t *testing.T) {
		defer cleanup()
		if fm.FileExists(nullFile) {
			t.Errorf("Expected fileExists(null) to return false")
		}
	})

	t.Run("testCreateFile_success", func(t *testing.T) {
		defer cleanup()
		created, err := fm.CreateFile(testFile)
		if !created || err != nil {
			t.Errorf("Expected createFile(%s) to create file, got %v, err=%v", testFile, created, err)
		}
		created, err = fm.CreateFile(testFile)
		if created || err != nil {
			t.Errorf("Expected createFile on existing file to return false and nil error, got %v, err=%v", created, err)
		}
	})

	t.Run("testCreateFile_null", func(t *testing.T) {
		defer cleanup()
		_, err := fm.CreateFile(nullFile)
		if err == nil {
			t.Fatalf("Expected error for createFile(null) but got none")
		}
	})

	t.Run("testDeleteFile_exists", func(t *testing.T) {
		defer cleanup()
		f, err := os.Create(testFile)
		if err != nil {
			t.Fatalf("Could not create file: %v", err)
		}
		f.Close()
		if !fm.DeleteFile(testFile) {
			t.Errorf("Expected deleteFile to return true")
		}
		if _, err := os.Stat(testFile); !os.IsNotExist(err) {
			t.Errorf("File %s should not exist after deletion", testFile)
		}
	})

	t.Run("testDeleteFile_notExists", func(t *testing.T) {
		defer cleanup()
		if fm.DeleteFile("dummy.txt") {
			t.Errorf("Expected deleteFile on non-existing file to return false")
		}
	})

	t.Run("testDeleteFile_null", func(t *testing.T) {
		defer cleanup()
		if fm.DeleteFile(nullFile) {
			t.Errorf("Expected deleteFile(null) to return false")
		}
	})

	t.Run("testCopyFile_success", func(t *testing.T) {
		defer cleanup()
		f, err := os.Create(testFile)
		if err != nil {
			t.Fatalf("Failed to create source file: %v", err)
		}
		f.Close()
		copied, err := fm.CopyFile(testFile, copiedFile)
		if !copied || err != nil {
			t.Errorf("Expected copyFile to succeed, got %v, err=%v", copied, err)
		}
	})

	t.Run("testCopyFile_sourceNull", func(t *testing.T) {
		defer cleanup()
		_, err := fm.CopyFile("", "dest.txt")
		if err == nil {
			t.Fatalf("Expected error for copyFile(source null)")
		}
	})

	t.Run("testCopyFile_destNull", func(t *testing.T) {
		defer cleanup()
		_, err := fm.CopyFile("src.txt", "")
		if err == nil {
			t.Fatalf("Expected error for copyFile(dest null)")
		}
	})
}