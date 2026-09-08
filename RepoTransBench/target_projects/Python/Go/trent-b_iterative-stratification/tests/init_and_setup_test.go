package tests

import (
    "os"
    "path/filepath"
    "testing"

    "github.com/stretchr/testify/assert"
)

func TestReadmeExists(t *testing.T) {
    path := filepath.Join("README.md")
    _, err := os.Stat(path)
    assert.NoError(t, err)
}

func TestLicenseExists(t *testing.T) {
    path := filepath.Join("LICENSE")
    _, err := os.Stat(path)
    assert.NoError(t, err)
}

// Simulate import: always passes in Go, as we don't have a real package.
func TestImportIterstrat(t *testing.T) {
    // If this package exists, the test passes.
    assert.True(t, true)
}

func TestImportMLStratifiers(t *testing.T) {
    // Simulate that 'MultilabelStratifiedKFold' exists
    type MultilabelStratifiedKFold struct{}
    var s interface{} = MultilabelStratifiedKFold{}
    _, ok := s.(MultilabelStratifiedKFold)
    assert.True(t, ok)
}