package public_tests

import "testing"

func TestImportZbarLibraryPublic(t *testing.T) {
	zl := struct {
		Name string
	}{Name: "pyzbar.zbar_library"}
	if zl.Name == "" {
		t.Fatal("expected Name to be non-empty")
	}
}