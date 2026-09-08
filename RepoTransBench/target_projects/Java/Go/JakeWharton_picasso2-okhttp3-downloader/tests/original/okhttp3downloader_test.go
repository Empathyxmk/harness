package original

import (
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestShutdownDoesNotThrow(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	downloader.Shutdown()
	// no assertion
}

func TestDummyConstructor(t *testing.T) {
	_ = picasso.NewOkHttp3DownloaderWithDummy("dummy")
	// no assertion, just makes sure constructor does not panic
}