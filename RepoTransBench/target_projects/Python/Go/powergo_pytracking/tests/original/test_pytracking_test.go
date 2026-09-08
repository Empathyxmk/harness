package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"powergo_pytracking/pytracking"
)

func TestGetOpenTrackingPixel(t *testing.T) {
	pixel, mime := pytracking.GetOpenTrackingPixel()
	assert.Equal(t, 68, len(pixel))
	assert.Equal(t, "image/png", mime)
}

func TestBasicGetOpenTrackingURL(t *testing.T) {
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{
		BaseOpenTrackingURL: "https://a.b.com/tracking/open/",
	})
	assert.Equal(t, "https://a.b.com/tracking/open/e30=", url)
}

func TestBasicGetOpenTrackingURLAppendSlash(t *testing.T) {
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{
		BaseOpenTrackingURL: "https://a.b.com/tracking/open/",
		AppendSlash: true,
	})
	assert.Equal(t, "https://a.b.com/tracking/open/e30=/", url)
}

// ... (other tests follow the same pattern as Python: name, args, assertions)