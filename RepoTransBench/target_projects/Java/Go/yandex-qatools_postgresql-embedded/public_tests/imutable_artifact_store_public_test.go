package public_tests

import (
	"testing"
)

type DummyMutableStore struct {
	removed       bool
	lastFileSetId string
}

func (s *DummyMutableStore) RemoveFileSet(fileSetId string) {
	s.removed = true
	s.lastFileSetId = fileSetId
}

func (s *DummyMutableStore) IsRemoved() bool {
	return s.removed
}

func (s *DummyMutableStore) GetLastFileSetId() string {
	return s.lastFileSetId
}

func TestCallsRemoveFileSetWithDifferentData(t *testing.T) {
	store := &DummyMutableStore{}
	store.RemoveFileSet("public-fileset-abc")
	if !store.IsRemoved() {
		t.Errorf("Expected IsRemoved true after RemoveFileSet call")
	}
	if store.GetLastFileSetId() != "public-fileset-abc" {
		t.Errorf("Expected lastFileSetId='public-fileset-abc', got '%s'", store.GetLastFileSetId())
	}
}

func TestRemoveFileSetNotCalledByDefault(t *testing.T) {
	store := &DummyMutableStore{}
	if store.IsRemoved() {
		t.Error("Expected IsRemoved false by default")
	}
	if store.GetLastFileSetId() != "" {
		t.Errorf("Expected GetLastFileSetId to be empty by default, got '%s'", store.GetLastFileSetId())
	}
}