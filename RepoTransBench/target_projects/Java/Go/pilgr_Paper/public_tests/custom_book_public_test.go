package public_tests

import (
	"strings"
	"testing"
	"pilgr_paper/tests/original"
)

func TestGetFolderPathForBookCustomPublic(t *testing.T) {
	path := "/io.paperdb.test/files/public_custom"
	if !strings.HasSuffix(path, "/io.paperdb.test/files/public_custom") {
		t.Errorf("Expected path to end with '/io.paperdb.test/files/public_custom', got %s", path)
	}
}

func TestGetFilePathForKeyCustomBookPublic(t *testing.T) {
	path := "/io.paperdb.test/files/public_custom/my_val.pt"
	if !strings.HasSuffix(path, "/io.paperdb.test/files/public_custom/my_val.pt") {
		t.Errorf("Expected path to end with '/io.paperdb.test/files/public_custom/my_val.pt', got %s", path)
	}
}

func TestReadWriteDeleteToDifferentBooksPublic(t *testing.T) {
	defaultBook := original.NewPaperStore()
	publicBook := original.NewPaperStore()
	defaultBook.Destroy()
	publicBook.Destroy()

	defaultBook.Write("country", "Denmark")
	publicBook.Write("country", "Norway")

	got1 := defaultBook.Read("country")
	got2 := publicBook.Read("country")
	if got1 != "Denmark" {
		t.Errorf("Expected Denmark, got %v", got1)
	}
	if got2 != "Norway" {
		t.Errorf("Expected Norway, got %v", got2)
	}

	defaultBook.Delete("country")
	if defaultBook.Contains("country") {
		t.Errorf("country still exists in defaultBook")
	}
	if !publicBook.Contains("country") {
		t.Errorf("country missing from publicBook")
	}
}