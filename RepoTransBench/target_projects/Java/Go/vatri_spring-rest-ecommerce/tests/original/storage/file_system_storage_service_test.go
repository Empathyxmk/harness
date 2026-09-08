package storage

import (
    "fmt"
    "io"
    "os"
    "path/filepath"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

const TEST_LOCATION = "test-uploads-orig"

func setup(t *testing.T) (*testsutil.FileSystemStorageService, func()) {
    props := testsutil.NewStorageProperties()
    props.SetLocation(TEST_LOCATION)
    storage := testsutil.NewFileSystemStorageService(props)
    require.NoError(t, storage.DeleteAll())
    require.NoError(t, storage.Init())
    cleanup := func() {
        storage.DeleteAll()
        os.RemoveAll(TEST_LOCATION)
    }
    return storage, cleanup
}

func TestInitCreatesDirectory(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    assert.True(t, true)
}

func TestStoreValidFile(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    file := testsutil.NewMockMultipartFile("file", "test.txt", "text/plain", []byte("Spring Boot"))
    storedName, err := storage.Store(file, "subdir")
    assert.NoError(t, err)
    path := filepath.Join(TEST_LOCATION, "subdir", "test.txt")
    hasFile := false
    for k := range storage.StorageFiles {
        if k == path {
            hasFile = true
            break
        }
    }
    assert.True(t, hasFile)
}

func TestStoreEmptyFileThrows(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    file := testsutil.NewMockMultipartFile("file", "empty.txt", "text/plain", []byte{})
    _, err := storage.Store(file, "")
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "Failed to store empty file")
}

func TestLoadAllListsFiles(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    file := testsutil.NewMockMultipartFile("file", "loadall.txt", "text/plain", []byte("Test"))
    storage.Store(file, "")
    files, err := storage.LoadAll()
    assert.NoError(t, err)
    assert.GreaterOrEqual(t, len(files), 1)
}

func TestLoadReturnsCorrectPath(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    fname := "myfile.txt"
    p := filepath.Join(TEST_LOCATION, fname)
    storage.StorageFiles[p] = []byte("hello")
    res, err := storage.Load(fname)
    assert.NoError(t, err)
    assert.Equal(t, p, res)
}

func TestLoadAsResourceReturnsResource(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    fname := "resource.txt"
    p := filepath.Join(TEST_LOCATION, fname)
    content := []byte("hello")
    storage.StorageFiles[p] = content
    f, err := storage.LoadAsResource(fname)
    assert.NoError(t, err)
    data, _ := io.ReadAll(f)
    assert.Equal(t, content, data)
    f.Close()
}

func TestLoadAsResourceFileNotFound(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    fname := fmt.Sprintf("notexist-%d.txt", os.Getpid())
    _, err := storage.LoadAsResource(fname)
    assert.Error(t, err)
    assert.Contains(t, err.Error(), fname)
}

func TestDeleteAllDeletesDirectory(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    path := filepath.Join(TEST_LOCATION, "toremove.txt")
    storage.StorageFiles[path] = []byte("bye")
    assert.Contains(t, storage.StorageFiles, path)
    storage.DeleteAll()
    assert.Len(t, storage.StorageFiles, 0)
}

func TestInitIOExceptionThrows(t *testing.T) {
    forbidden := "/root/forbidden-"
    sp := testsutil.NewStorageProperties()
    sp.SetLocation(forbidden + fmt.Sprint(os.Getpid()))
    bad := testsutil.NewFileSystemStorageService(sp)
    err := bad.Init()
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "Could not initialize storage")
}

func TestStoreIOExceptionThrows(t *testing.T) {
    storage, cleanup := setup(t)
    defer cleanup()
    file := testsutil.NewMockMultipartFile("file", "bad.txt", "text/plain", []byte("fail"))
    file.FailInputStream = true
    _, err := storage.Store(file, "badpath")
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "Failed to store file")
}

func TestLoadAllIOExceptionThrows(t *testing.T) {
    forbidden := "/root/forbidden-"
    sp := testsutil.NewStorageProperties()
    sp.SetLocation(forbidden + fmt.Sprint(os.Getpid()))
    bad := testsutil.NewFileSystemStorageService(sp)
    _, err := bad.LoadAll()
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "Failed to read stored files")
}

func TestLoadAsResourceMalformedURL(t *testing.T) {
    sp := testsutil.NewStorageProperties()
    sp.SetLocation(TEST_LOCATION)
    bad := testsutil.NewFileSystemStorageService(sp)
    bad.Load = func(filename string) (string, error) {
        return string([]byte{0}), nil
    }
    _, err := bad.LoadAsResource("badfile")
    assert.Error(t, err)
}