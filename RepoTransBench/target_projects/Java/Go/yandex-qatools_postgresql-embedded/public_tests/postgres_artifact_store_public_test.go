package public_tests

import (
	"testing"
)

type PostgresArtifactStoreFake struct {
	artifact string
}

func NewPostgresArtifactStoreFake(artifact string) *PostgresArtifactStoreFake {
	return &PostgresArtifactStoreFake{
		artifact: artifact,
	}
}

func (s *PostgresArtifactStoreFake) GetArtifact() string {
	return s.artifact
}

func (s *PostgresArtifactStoreFake) SetArtifact(artifact string) {
	s.artifact = artifact
}

func TestStoresArtifactNameWithDifferentValue(t *testing.T) {
	store := NewPostgresArtifactStoreFake("public-art-unique-192")
	if store.GetArtifact() != "public-art-unique-192" {
		t.Errorf("Expected artifact to be 'public-art-unique-192', got '%s'", store.GetArtifact())
	}
}

func TestSetArtifactUpdatesArtifactWithAnotherValue(t *testing.T) {
	store := NewPostgresArtifactStoreFake("start-art-public-1")
	store.SetArtifact("set-artifact-public-2")
	if store.GetArtifact() != "set-artifact-public-2" {
		t.Errorf("Expected artifact to be 'set-artifact-public-2', got '%s'", store.GetArtifact())
	}
}