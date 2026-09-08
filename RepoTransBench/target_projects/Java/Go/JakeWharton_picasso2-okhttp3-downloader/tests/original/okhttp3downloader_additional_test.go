package original

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestLoadSucceedsWithDifferentNetworkPolicies(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	tests := []struct {
		url    string
		policy int
	}{
		{"http://localhost/ok", 0},
		{"http://localhost/ok", -1},
		{"http://localhost/ok", 123},
	}
	for _, tc := range tests {
		r, err := downloader.Load(tc.url, tc.policy)
		if err != nil || r == nil {
			t.Errorf("Expected successful load for url=%s, policy=%d, got error: %v", tc.url, tc.policy, err)
		}
	}
}

func TestShutdownMultipleTimes(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	downloader.Shutdown()
	downloader.Shutdown() // Should not panic or error
}

func TestLoadThrowsWhenUrlIsEmpty(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	_, err := downloader.Load("", 0)
	if err == nil {
		t.Fatalf("Expected error when loading empty url")
	}
}

func TestAllConstructorsWithShutdown(t *testing.T) {
	// /tmp/cacheA and B may not exist, but these are safe as File pointers aren't used
	fileA := mustTempFile(t, "cacheA")
	fileB := mustTempFile(t, "cacheB")
	defer os.Remove(fileA.Name())
	defer os.Remove(fileB.Name())

	d1 := picasso.NewOkHttp3DownloaderWithFileAndMaxSize(fileA, 5)
	d2 := picasso.NewOkHttp3DownloaderWithFile(fileB)
	d3 := picasso.NewOkHttp3DownloaderWithMaxSize(123)
	d4 := picasso.NewOkHttp3Downloader()
	d5 := picasso.NewOkHttp3DownloaderWithDummy("dummy2")

	d1.Shutdown()
	d2.Shutdown()
	d3.Shutdown()
	d4.Shutdown()
	d5.Shutdown()
}

func mustTempFile(t *testing.T, name string) *os.File {
	f, err := os.CreateTemp(os.TempDir(), name)
	if err != nil {
		t.Fatalf("could not create temp file: %v", err)
	}
	return f
}