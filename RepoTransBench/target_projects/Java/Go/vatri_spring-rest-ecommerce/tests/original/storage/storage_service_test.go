package storage

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

type MyStorageService struct{}

func (m *MyStorageService) Init() error { return nil }
func (m *MyStorageService) Store(f testsutil.MultipartFile, s string) (string, error) {
    return "ok", nil
}
func (m *MyStorageService) LoadAll() ([]string, error) { return []string{}, nil }
func (m *MyStorageService) Load(file string) (string, error) { return "", nil }
func (m *MyStorageService) LoadAsResource(file string) (*testsutil.MockReader, error) { return nil, nil }
func (m *MyStorageService) DeleteAll() error { return nil }

func TestDummyInterfaceImplementation(t *testing.T) {
    var s testsutil.StorageService = &MyStorageService{}
    require.NotNil(t, s)
    assert.NoError(t, s.Init())
    v, err := s.Store(nil, "")
    assert.Equal(t, "ok", v)
    files, err := s.LoadAll()
    assert.NotNil(t, files)
    path, err := s.Load("")
    assert.Equal(t, "", path)
    res, err := s.LoadAsResource("")
    assert.Nil(t, res)
    assert.NoError(t, s.DeleteAll())
}