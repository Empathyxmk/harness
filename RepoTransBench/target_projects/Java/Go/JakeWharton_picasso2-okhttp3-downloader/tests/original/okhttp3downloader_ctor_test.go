package original

import (
	"testing"

	"github.com/jakewharton/picasso2-okhttp3-downloader/picasso"
)

func TestNoArgCtor(t *testing.T) {
	_ = picasso.NewOkHttp3Downloader()
}