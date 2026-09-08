package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"powergo_pytracking/pytracking"
)

func TestPublicInitExportsAccess(t *testing.T) {
	assert.IsType(t, &pytracking.Configuration{}, pytracking.NewConfiguration(pytracking.ConfigurationArgs{}))
	assert.IsType(t, []byte{}, pytracking.TrackingPixel)
	assert.IsType(t, "", pytracking.PNGMimeType)
	assert.IsType(t, 0, pytracking.DefaultTimeoutSeconds)
	assert.NotNil(t, pytracking.GetClickTrackingURL)
	assert.NotNil(t, pytracking.GetClickTrackingResult)
	assert.NotNil(t, pytracking.GetOpenTrackingResult)
	assert.NotNil(t, pytracking.GetOpenTrackingURL)
	assert.NotNil(t, pytracking.GetOpenTrackingURLPath)
	assert.NotNil(t, pytracking.GetClickTrackingURLPath)
	assert.NotNil(t, pytracking.GetOpenTrackingPixel)
}