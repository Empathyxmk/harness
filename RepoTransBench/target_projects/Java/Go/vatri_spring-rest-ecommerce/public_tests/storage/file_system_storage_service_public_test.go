package storage

import (
    "io"
    "os"
    "path/filepath"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

const testLocation = "test-public-upload-dir"

func setupPublic(t *testing.T) (*testsutil.FileSystemStorageService, func()) {
    props := testsutil.NewStorageProperties()
    props.SetLocation(testLocation)
    storage := testsutil.NewFileSystemStorageService(props)
    require.NoError(t, storage.DeleteAll())
    require.NoError(t, storage.Init())
    cleanup := func() {
        storage.DeleteAll()
        os.RemoveAll(testLocation)
    }
    return storage, cleanup
}

func TestStoreAndLoadPublicFile(t *testing.T) {
    storage, cleanup := setupPublic(t)
    defer cleanup()
    file := testsutil.NewMockMultipartFile("publicfile", "publicfile.txt", "text/plain", []byte("test public content"))

    storedFileName, err := storage.Store(file, "publicfile.txt")
    require.NoError(t, err)
    assert.Equal(t, "publicfile.txt", storedFileName)

    loadedPath, err := storage.Load("publicfile.txt")
    require.NoError(t, err)
    assert.Equal(t, filepath.Join(testLocation, "publicfile.txt"), loadedPath)

    f, err := storage.LoadAsResource("publicfile.txt")
    require.NoError(t, err)
    assert.NotNil(t, f)
    data, _ := io.ReadAll(f)
    assert.Equal(t, []byte("test public content"), data)
    f.Close()

    files, err := storage.LoadAll()
    require.NoError(t, err)
    found := false
    for _, p := range files {
        if filepath.Base(p) == "publicfile.txt" {
            found = true
            break
        }
    }
    assert.True(t, found)
}

func TestDeleteAllPublic(t *testing.T) {
    storage, cleanup := setupPublic(t)
    defer cleanup()
    p := filepath.Join(testLocation, "todelete-public.txt")
    storage.StorageFiles[p] = []byte("dummy")
    assert.Contains(t, storage.StorageFiles, p)
    storage.DeleteAll()
    assert.NotContains(t, storage.StorageFiles, p)
}