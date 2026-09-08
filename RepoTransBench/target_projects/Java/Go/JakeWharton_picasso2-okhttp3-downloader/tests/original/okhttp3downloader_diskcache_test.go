package original

import (
	"os"
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestCtorWithCacheDir(t *testing.T) {
	tmpfile := mustTempFile(t, "cache")
	defer os.Remove(tmpfile.Name())
	_ = picasso.NewOkHttp3DownloaderWithFile(tmpfile)
	// just construct, no assert
}

func TestCtorWithCacheDirAndMaxSize(t *testing.T) {
	tmpfile := mustTempFile(t, "cache")
	defer os.Remove(tmpfile.Name())
	_ = picasso.NewOkHttp3DownloaderWithFileAndMaxSize(tmpfile, 1024)
}

func TestCtorWithMaxSize(t *testing.T) {
	_ = picasso.NewOkHttp3DownloaderWithMaxSize(4096)
}

func mustTempFile(t *testing.T, name string) *os.File {
	f, err := os.CreateTemp(os.TempDir(), name)
	if err != nil {
		t.Fatalf("could not create temp file: %v", err)
	}
	return f
}