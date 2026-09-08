package public_tests

import (
	"os"
	"testing"
)

func TestMetaPublicTest_ProjectRequiredFilesExist_Public(t *testing.T) {
	if _, err := os.Stat("pom.xml"); err != nil {
		t.Errorf("pom.xml must be present in the repo, err: %v", err)
	}
	if _, err := os.Stat("LICENSE"); err != nil {
		t.Errorf("LICENSE should exist in project root, err: %v", err)
	}
}