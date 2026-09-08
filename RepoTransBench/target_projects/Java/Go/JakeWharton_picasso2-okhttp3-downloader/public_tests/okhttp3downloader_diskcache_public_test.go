package public_tests

import (
	"os"
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestCtorWithAnotherCacheDir(t *testing.T) {
	file := mustTempFile(t, "pub_cache_c")
	defer os.Remove(file.Name())
	_ = picasso.NewOkHttp3DownloaderWithFile(file)
}

func TestCtorWithAnotherCacheDirAndMaxSize(t *testing.T) {
	file := mustTempFile(t, "pub_cache_d")
	defer os.Remove(file.Name())
	_ = picasso.NewOkHttp3DownloaderWithFileAndMaxSize(file, 5555)
}

func TestCtorWithAnotherMaxSize(t *testing.T) {
	_ = picasso.NewOkHttp3DownloaderWithMaxSize(9876)
}

func mustTempFile(t *testing.T, name string) *os.File {
	f, err := os.CreateTemp(os.TempDir(), name)
	if err != nil {
		t.Fatalf("could not create temp file: %v", err)
	}
	return f
}