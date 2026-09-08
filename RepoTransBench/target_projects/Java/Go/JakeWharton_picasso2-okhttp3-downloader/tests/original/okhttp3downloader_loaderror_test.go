package original

import (
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestLoadThrowsOnNullUrl(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	_, err := downloader.Load("", 0)
	if err == nil {
		t.Fatal("expected error when loading null/empty url")
	}
}

func TestLoadThrowsOnInvalidUrl(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	_, err := downloader.Load("ftp://localhost/abc", 0)
	if err == nil {
		t.Fatalf("expected error for invalid protocol url")
	}
}

func TestLoadSucceedsOnValidUrl(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	r, err := downloader.Load("http://localhost/abc", 0)
	if err != nil || r == nil {
		t.Fatalf("expected successful load for valid url, got err=%v", err)
	}
}