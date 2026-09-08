package public_tests

import (
	"testing"
	"strings"
	"powergo_pytracking/pytracking"
	"github.com/stretchr/testify/assert"
)

func TestPublicGetOpenTrackingPixel(t *testing.T) {
	pixel, mime := pytracking.GetOpenTrackingPixel()
	assert.IsType(t, []byte{}, pixel)
	assert.Equal(t, "image/png", mime)
}

func TestPublicBasicGetOpenTrackingURL(t *testing.T) {
	const baseURL = "https://y.z.com/track/open/"
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{
		BaseOpenTrackingURL: baseURL,
	})
	assert.True(t, strings.HasPrefix(url, baseURL))
	assert.NotEqual(t, "", url[len(baseURL):])
}

func TestPublicBasicGetOpenTrackingURLAppendSlash(t *testing.T) {
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{
		BaseOpenTrackingURL: "https://y.z.com/track/open/",
		AppendSlash: true,
	})
	assert.True(t, strings.HasSuffix(url, "/"))
}

func TestPublicInConfigOpenTrackingURL(t *testing.T) {
	base := "https://y.z.com/track/open/"
	webhook := "https://notify.me/webhook/"
	// using dummy metadata for test
	altMetadata := map[string]interface{}{"param4": "val4", "another": true, "nested_alt": map[string]interface{}{"paramA": "valA"}}
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{
		BaseOpenTrackingURL: base,
		Metadata:            altMetadata,
	})
	path := pytracking.GetOpenTrackingURLPath(url, pytracking.OpenTrackingURLArgs{BaseOpenTrackingURL: base})

	trackingResult := pytracking.GetOpenTrackingResult(path, pytracking.OpenTrackingResultArgs{WebhookURL: webhook})
	assert.Nil(t, trackingResult.TrackedURL)
	assert.Equal(t, webhook, trackingResult.WebhookURL)
	assert.Nil(t, trackingResult.RequestData)
	assert.Equal(t, altMetadata, trackingResult.Metadata)
	assert.True(t, trackingResult.IsOpenTracking)
	assert.False(t, trackingResult.IsClickTracking)
}

func TestPublicInConfigOpenTrackingURLToJson(t *testing.T) {
	base := "https://y.z.com/track/open/"
	webhook := "https://notify.me/webhook/"
	altMetadata := map[string]interface{}{"param4": "val4", "another": true, "nested_alt": map[string]interface{}{"paramA": "valA"}}
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{BaseOpenTrackingURL: base, Metadata: altMetadata})
	path := pytracking.GetOpenTrackingURLPath(url, pytracking.OpenTrackingURLArgs{BaseOpenTrackingURL: base})

	tr := pytracking.GetOpenTrackingResult(path, pytracking.OpenTrackingResultArgs{WebhookURL: webhook})
	trDict := tr.ToJSONDict()
	assert.Nil(t, trDict["tracked_url"])
	assert.Equal(t, webhook, trDict["webhook_url"])
	assert.Nil(t, trDict["request_data"])
	assert.Equal(t, altMetadata, trDict["metadata"])
	assert.True(t, trDict["is_open_tracking"].(bool))
	assert.False(t, trDict["is_click_tracking"].(bool))
}

func TestPublicInConfigOpenTrackingFullURL(t *testing.T) {
	base := "https://y.z.com/track/open/"
	webhook := "https://notify.me/webhook/"
	altMetadata := map[string]interface{}{"param4": "val4", "another": true, "nested_alt": map[string]interface{}{"paramA": "valA"}}
	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{BaseOpenTrackingURL: base, Metadata: altMetadata})
	trackingResult := pytracking.GetOpenTrackingResult(url, pytracking.OpenTrackingResultArgs{WebhookURL: webhook, BaseOpenTrackingURL: base})
	assert.Nil(t, trackingResult.TrackedURL)
	assert.Equal(t, webhook, trackingResult.WebhookURL)
	assert.Nil(t, trackingResult.RequestData)
	assert.Equal(t, altMetadata, trackingResult.Metadata)
	assert.True(t, trackingResult.IsOpenTracking)
	assert.False(t, trackingResult.IsClickTracking)
}

func TestPublicEmbeddedOpenTrackingURL(t *testing.T) {
	base := "https://y.z.com/track/open/"
	webhook := "https://notify.me/webhook/"
	altMetadata := map[string]interface{}{"param4": "val4", "another": true, "nested_alt": map[string]interface{}{"paramA": "valA"}}
	altDefaultMeta := map[string]interface{}{"key42": false, "strangeé": "winoèèè", "paramX": "other3"}
	altExpectedMeta := make(map[string]interface{})
	for k, v := range altDefaultMeta {
		altExpectedMeta[k] = v
	}
	for k, v := range altMetadata {
		altExpectedMeta[k] = v
	}
	altRequestData := map[string]interface{}{"user_agent": "Safari", "user_ip": "192.168.1.1"}

	url := pytracking.GetOpenTrackingURL(pytracking.OpenTrackingURLArgs{
		BaseOpenTrackingURL: base,
		WebhookURL:          webhook,
		IncludeWebhookURL:   true,
		DefaultMetadata:     altDefaultMeta,
		IncludeDefaultMetadata: true,
		Metadata:            altMetadata,
	})
	path := pytracking.GetOpenTrackingURLPath(url, pytracking.OpenTrackingURLArgs{BaseOpenTrackingURL: base})

	trackingResult := pytracking.GetOpenTrackingResult(path, pytracking.OpenTrackingResultArgs{
		RequestData:          altRequestData,
		IncludeDefaultMetadata: true,
		IncludeWebhookURL:    true,
	})
	assert.Nil(t, trackingResult.TrackedURL)
	assert.Equal(t, webhook, trackingResult.WebhookURL)
	assert.Equal(t, altRequestData, trackingResult.RequestData)
	assert.Equal(t, altExpectedMeta, trackingResult.Metadata)
	assert.True(t, trackingResult.IsOpenTracking)
	assert.False(t, trackingResult.IsClickTracking)
}

func TestPublicBasicGetClickTrackingURL(t *testing.T) {
	const BASE_URL = "https://y.z.com/track/"
	const ALT_URL_TO_TRACK = "https://anotherdomain.io/tracking/?data=newdata"
	url := pytracking.GetClickTrackingURL(pytracking.ClickTrackingURLArgs{
		URL: ALT_URL_TO_TRACK,
		BaseClickTrackingURL: BASE_URL,
	})
	assert.True(t, strings.HasPrefix(url, BASE_URL))
	assert.Contains(t, url, "=")
}

func TestPublicBasicGetClickTrackingURLAppendSlash(t *testing.T) {
	const BASE_URL = "https://y.z.com/track/"
	const ALT_URL_TO_TRACK = "https://anotherdomain.io/tracking/?data=newdata"
	url := pytracking.GetClickTrackingURL(pytracking.ClickTrackingURLArgs{
		URL: ALT_URL_TO_TRACK,
		BaseClickTrackingURL: BASE_URL,
		AppendSlash:          true,
	})
	assert.True(t, strings.HasSuffix(url, "/"))
}

func TestPublicInConfigClickTrackingURL(t *testing.T) {
	const BASE_URL = "https://y.z.com/track/"
	const ALT_URL_TO_TRACK = "https://anotherdomain.io/tracking/?data=newdata"
	const WEBHOOK = "https://notify.me/webhook/"
	altMetadata := map[string]interface{}{"param4": "val4", "another": true, "nested_alt": map[string]interface{}{"paramA": "valA"}}
	url := pytracking.GetClickTrackingURL(pytracking.ClickTrackingURLArgs{
		URL: ALT_URL_TO_TRACK,
		BaseClickTrackingURL: BASE_URL,
		Metadata:             altMetadata,
	})
	path := pytracking.GetClickTrackingURLPath(url, pytracking.ClickTrackingURLArgs{BaseClickTrackingURL: BASE_URL})
	trackingResult := pytracking.GetClickTrackingResult(path, pytracking.ClickTrackingResultArgs{WebhookURL: WEBHOOK})

	assert.Equal(t, ALT_URL_TO_TRACK, trackingResult.TrackedURL)
	assert.Equal(t, WEBHOOK, trackingResult.WebhookURL)
	assert.Nil(t, trackingResult.RequestData)
	assert.Equal(t, altMetadata, trackingResult.Metadata)
	assert.True(t, trackingResult.IsClickTracking)
	assert.False(t, trackingResult.IsOpenTracking)
}

func TestPublicInConfigClickTrackingFullURL(t *testing.T) {
	const BASE_URL = "https://y.z.com/track/"
	const ALT_URL_TO_TRACK = "https://anotherdomain.io/tracking/?data=newdata"
	const WEBHOOK = "https://notify.me/webhook/"
	altMetadata := map[string]interface{}{"param4": "val4", "another": true, "nested_alt": map[string]interface{}{"paramA": "valA"}}
	url := pytracking.GetClickTrackingURL(pytracking.ClickTrackingURLArgs{
		URL: ALT_URL_TO_TRACK,
		BaseClickTrackingURL: BASE_URL,
		Metadata:             altMetadata,
	})
	trackingResult := pytracking.GetClickTrackingResult(url, pytracking.ClickTrackingResultArgs{
		WebhookURL:          WEBHOOK,
		BaseClickTrackingURL: BASE_URL,
	})
	assert.Equal(t, ALT_URL_TO_TRACK, trackingResult.TrackedURL)
	assert.Equal(t, WEBHOOK, trackingResult.WebhookURL)
	assert.Nil(t, trackingResult.RequestData)
	assert.Equal(t, altMetadata, trackingResult.Metadata)
	assert.True(t, trackingResult.IsClickTracking)
	assert.False(t, trackingResult.IsOpenTracking)
}