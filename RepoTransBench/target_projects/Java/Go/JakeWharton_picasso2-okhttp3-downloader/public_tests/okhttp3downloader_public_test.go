package public_tests

import (
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestShutdownIsSafeRepeatedly(t *testing.T) {
	downloader := picasso.NewOkHttp3Downloader()
	downloader.Shutdown()
	downloader.Shutdown()
}

func TestAnotherDummyConstructor(t *testing.T) {
	_ = picasso.NewOkHttp3DownloaderWithDummy("publicValue")
}