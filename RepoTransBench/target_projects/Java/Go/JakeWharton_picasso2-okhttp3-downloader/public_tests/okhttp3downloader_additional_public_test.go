package public_tests

import (
	"os"
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestLoadSucceedsWithOtherNetworkPolicies(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	tests := []struct {
		url    string
		policy int
	}{
		{"http://127.0.0.1/success", 1},
		{"http://127.0.0.1/success", 42},
		{"http://127.0.0.1/success", -100},
	}
	for _, tc := range tests {
		r, err := downloader.Load(tc.url, tc.policy)
		if err != nil || r == nil {
			t.Errorf("Expected successful load for url=%s, policy=%d, got error: %v", tc.url, tc.policy, err)
		}
	}
}

func TestShutdownManyTimes(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	downloader.Shutdown()
	downloader.Shutdown()
	downloader.Shutdown() // extra, should not panic/error
}

func TestLoadThrowsWhenUrlIsNullString(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	_, err := downloader.Load("", 0)
	if err == nil {
		t.Fatalf("Expected error when loading null/empty url string")
	}
}

func TestAllConstructorsWithShutdownPublic(t *testing.T) {
	fileA := mustTempFile(t, "pub_cacheA")
	fileB := mustTempFile(t, "pub_cacheB")
	defer os.Remove(fileA.Name())
	defer os.Remove(fileB.Name())

	d1 := picasso.NewOkHttp3DownloaderWithFileAndMaxSize(fileA, 15)
	d2 := picasso.NewOkHttp3DownloaderWithFile(fileB)
	d3 := picasso.NewOkHttp3DownloaderWithMaxSize(321)
	d4 := picasso.NewOkHttp3Downloader()
	d5 := picasso.NewOkHttp3DownloaderWithDummy("publicDummy")

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