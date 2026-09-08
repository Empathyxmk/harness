package storage

import (
    "testing"
    "path/filepath"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

type MyStorageServicePublic struct{}

func (m *MyStorageServicePublic) Init() error { return nil }
func (m *MyStorageServicePublic) Store(f testsutil.MultipartFile, s string) (string, error) {
    return "public-ok", nil
}
func (m *MyStorageServicePublic) LoadAll() ([]string, error) {
    return []string{filepath.Join(".", "publicfile")}, nil
}
func (m *MyStorageServicePublic) Load(file string) (string, error) {
    return filepath.Join(".", "publicfile"), nil
}
func (m *MyStorageServicePublic) LoadAsResource(file string) (*testsutil.MockReader, error) {
    return nil, nil
}
func (m *MyStorageServicePublic) DeleteAll() error { return nil }

func TestDummyInterfaceImplementationDifferentData(t *testing.T) {
    var s testsutil.StorageService = &MyStorageServicePublic{}
    require.NotNil(t, s)
    assert.NoError(t, s.Init())
    v, err := s.Store(nil, "public")
    assert.Equal(t, "public-ok", v)
    files, err := s.LoadAll()
    assert.NotNil(t, files)
    assert.True(t, len(files) > 0)
    path, err := s.Load("public")
    assert.Equal(t, filepath.Join(".", "publicfile"), path)
    res, err := s.LoadAsResource("public")
    assert.Nil(t, res)
    assert.NoError(t, s.DeleteAll())
}