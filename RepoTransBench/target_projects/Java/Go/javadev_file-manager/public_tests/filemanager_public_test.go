package public_tests

import (
	"os"
	"testing"

	"filemanager"
)

func removeIfExistsPublic(t *testing.T, filename string) {
	if filename == "" {
		return
	}
	if _, err := os.Stat(filename); err == nil {
		if err := os.Remove(filename); err != nil {
			t.Fatalf("Failed to clean up file %s: %v", filename, err)
		}
	}
}

func TestFileManagerPublicTestSuite(t *testing.T) {
	fm := &filemanager.FileManager{}
	publicTestFile := "public_sample.txt"
	publicCopiedFile := "public_copied.txt"
	var publicNullFile string // "" is the closest analog to Java null

	cleanup := func() {
		removeIfExistsPublic(t, publicTestFile)
		removeIfExistsPublic(t, publicCopiedFile)
		removeIfExistsPublic(t, "unused_public.txt")
		removeIfExistsPublic(t, "another_public.txt")
	}

	t.Run("testFileExists_false_public", func(t *testing.T) {
		defer cleanup()
		if fm.FileExists("definitelynotexisting_public.txt") {
			t.Errorf("Expected file to not exist")
		}
	})

	t.Run("testFileExists_true_public", func(t *testing.T) {
		defer cleanup()
		f, err := os.Create(publicTestFile)
		if err != nil {
			t.Fatalf("Could not create file: %v", err)
		}
		f.Close()
		if !fm.FileExists(publicTestFile) {
			t.Errorf("Expected file to exist")
		}
	})

	t.Run("testFileExists_null_public", func(t *testing.T) {
		defer cleanup()
		if fm.FileExists(publicNullFile) {
			t.Errorf("Expected fileExists(null) to return false")
		}
	})

	t.Run("testCreateFile_success_public", func(t *testing.T) {
		defer cleanup()
		created, err := fm.CreateFile(publicTestFile)
		if !created || err != nil {
			t.Errorf("Expected createFile(%s) to create file, got %v, err=%v", publicTestFile, created, err)
		}
		created, err = fm.CreateFile(publicTestFile)
		if created || err != nil {
			t.Errorf("Expected createFile on existing file to return false and nil error, got %v, err=%v", created, err)
		}
	})

	t.Run("testCreateFile_null_public", func(t *testing.T) {
		defer cleanup()
		_, err := fm.CreateFile(publicNullFile)
		if err == nil {
			t.Fatalf("Expected error for createFile(null) but got none")
		}
	})

	t.Run("testDeleteFile_exists_public", func(t *testing.T) {
		defer cleanup()
		f, err := os.Create(publicTestFile)
		if err != nil {
			t.Fatalf("Could not create file: %v", err)
		}
		f.Close()
		if !fm.DeleteFile(publicTestFile) {
			t.Errorf("Expected deleteFile to return true")
		}
		if _, err := os.Stat(publicTestFile); !os.IsNotExist(err) {
			t.Errorf("File %s should not exist after deletion", publicTestFile)
		}
	})

	t.Run("testDeleteFile_notExists_public", func(t *testing.T) {
		defer cleanup()
		if fm.DeleteFile("unused_public.txt") {
			t.Errorf("Expected deleteFile on non-existing file to return false")
		}
	})

	t.Run("testDeleteFile_null_public", func(t *testing.T) {
		defer cleanup()
		if fm.DeleteFile(publicNullFile) {
			t.Errorf("Expected deleteFile(null) to return false")
		}
	})

	t.Run("testCopyFile_success_public", func(t *testing.T) {
		defer cleanup()
		f, err := os.Create(publicTestFile)
		if err != nil {
			t.Fatalf("Failed to create source file: %v", err)
		}
		f.Close()
		copied, err := fm.CopyFile(publicTestFile, publicCopiedFile)
		if !copied || err != nil {
			t.Errorf("Expected copyFile to succeed, got %v, err=%v", copied, err)
		}
	})

	t.Run("testCopyFile_sourceNull_public", func(t *testing.T) {
		defer cleanup()
		_, err := fm.CopyFile("", "another_public.txt")
		if err == nil {
			t.Fatalf("Expected error for copyFile(source null)")
		}
	})

	t.Run("testCopyFile_destNull_public", func(t *testing.T) {
		defer cleanup()
		_, err := fm.CopyFile("another_public.txt", "")
		if err == nil {
			t.Fatalf("Expected error for copyFile(dest null)")
		}
	})
}