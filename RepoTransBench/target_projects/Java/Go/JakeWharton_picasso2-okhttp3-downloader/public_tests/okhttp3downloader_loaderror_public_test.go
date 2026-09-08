package public_tests

import (
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestLoadThrowsOnInvalidProtocol(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	_, err := downloader.Load("ftp://someurl", 0)
	if err == nil {
		t.Fatalf("Expected error loading ftp://someurl due to protocol restrictions")
	}
}