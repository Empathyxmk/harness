package original

import (
	"bytes"
	"errors"
	"io"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

// --- Stubs ---

type ContextStub struct {
	assets *AssetManagerStub
}

func (c *ContextStub) GetAssets() *AssetManagerStub {
	return c.assets
}

type AssetManagerStub struct {
	contents map[string]interface{}
	open     func(string) (io.Reader, error)
	list     func(string) ([]string, error)
}

func (a *AssetManagerStub) List(path string) ([]string, error) {
	if a.list != nil {
		return a.list(path)
	}
	if files, ok := a.contents[path].([]string); ok {
		return files, nil
	}
	return nil, errors.New("not found")
}

func (a *AssetManagerStub) Open(name string) (io.Reader, error) {
	if a.open != nil {
		return a.open(name)
	}
	if buf, ok := a.contents[name].([]byte); ok {
		return bytes.NewReader(buf), nil
	}
	return nil, errors.New("not found")
}

// --- AssetsUtil implementation ---

func exportFiles(ctx *ContextStub, src string, dst string, am *AssetManagerStub) error {
	files, err := am.List(src)
	if err != nil {
		return err
	}
	if len(files) == 0 {
		reader, err := am.Open(src)
		if err != nil {
			return err
		}
		f, err := os.Create(dst)
		if err != nil {
			return err
		}
		defer f.Close()
		_, err = io.Copy(f, reader)
		return err
	}
	for _, f := range files {
		_ = os.MkdirAll(dst, 0755)
		reader, err := am.Open(src + "/" + f)
		if err == nil {
			outf, _ := os.Create(filepath.Join(dst, f))
			io.Copy(outf, reader)
			outf.Close()
		}
	}
	return nil
}

// --- TESTS ---

func TestAssetsUtil_ExportFiles_Directory(t *testing.T) {
	am := &AssetManagerStub{
		list: func(path string) ([]string, error) {
			if path == "src" {
				return []string{"f1", "f2"}, nil
			}
			return []string{}, nil
		},
		open: func(name string) (io.Reader, error) {
			return bytes.NewReader([]byte("content")), nil
		},
	}
	ctx := &ContextStub{assets: am}
	tempdir := filepath.Join(os.TempDir(), "assetsutiltest")
	_ = os.MkdirAll(tempdir, 0755)
	defer os.RemoveAll(tempdir)
	err := exportFiles(ctx, "src", tempdir, am)
	assert.NoError(t, err)
	_, err = os.Stat(tempdir)
	assert.NoError(t, err)
}

func TestAssetsUtil_ExportFiles_EmptyFile(t *testing.T) {
	am := &AssetManagerStub{
		list: func(path string) ([]string, error) {
			if path == "foo" {
				return []string{}, nil
			}
			return nil, errors.New("notfound")
		},
		open: func(name string) (io.Reader, error) {
			return bytes.NewReader([]byte("ok")), nil
		},
	}
	ctx := &ContextStub{assets: am}
	tempfile, _ := os.CreateTemp("", "AssetsUtilTest*.tmp")
	tempfile.Close()
	err := exportFiles(ctx, "foo", tempfile.Name(), am)
	assert.NoError(t, err)
	fi, err := os.Stat(tempfile.Name())
	assert.NoError(t, err)
	assert.Equal(t, int64(2), fi.Size())
	os.Remove(tempfile.Name())
}

func TestAssetsUtil_ExportFiles_IOException(t *testing.T) {
	am := &AssetManagerStub{
		list: func(path string) ([]string, error) {
			return nil, errors.New("failtest")
		},
	}
	ctx := &ContextStub{assets: am}
	err := exportFiles(ctx, "bad", "/tmp/notused", am)
	assert.Error(t, err)
}