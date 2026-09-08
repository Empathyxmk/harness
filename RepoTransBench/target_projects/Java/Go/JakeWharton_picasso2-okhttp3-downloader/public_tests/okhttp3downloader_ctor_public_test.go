package public_tests

import (
	"os"
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestPublicCtorWithCacheDir(t *testing.T) {
	file := mustTempFile(t, "public_ctor_cache")
	defer os.Remove(file.Name())
	_ = picasso.NewOkHttp3DownloaderWithFile(file)
}

func TestPublicCtorWithCacheDirAndMaxSize(t *testing.T) {
	file := mustTempFile(t, "public_ctor_cache2")
	defer os.Remove(file.Name())
	_ = picasso.NewOkHttp3DownloaderWithFileAndMaxSize(file, 2048)
}

func TestPublicCtorWithMaxSize(t *testing.T) {
	_ = picasso.NewOkHttp3DownloaderWithMaxSize(8192)
}

func mustTempFile(t *testing.T, name string) *os.File {
	f, err := os.CreateTemp(os.TempDir(), name)
	if err != nil {
		t.Fatalf("could not create temp file: %v", err)
	}
	return f
}