package public_tests

import (
	"testing"
	"bumpversion"
)

func TestKnownVCSMappingsNonGitMercurial(t *testing.T) {
	vcsMap := bumpversion.KnownVCS()
	if _, ok := vcsMap["hg"]; !ok {
		t.Errorf("Expected vcsMap to contain 'hg'")
	}
	if _, ok := vcsMap["svn"]; !ok {
		t.Errorf("Expected vcsMap to contain 'svn'")
	}
}

func TestVCSMapContentTypes(t *testing.T) {
	vcsMap := bumpversion.KnownVCS()
	for k, v := range vcsMap {
		if k == "" {
			t.Errorf("Expected VCS key to be non-empty string")
		}
		if v == nil {
			t.Errorf("Expected callable value, got nil")
		}
	}
}

func TestDefaultVCSScenarios(t *testing.T) {
	vcsMap := bumpversion.KnownVCS()
	if _, ok := vcsMap["hg"]; !ok {
		if _, oksvn := vcsMap["svn"]; !oksvn {
			t.Errorf("Expected vcsMap to contain either 'hg' or 'svn'")
		}
	}
}