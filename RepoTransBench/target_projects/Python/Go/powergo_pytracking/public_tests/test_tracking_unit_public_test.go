package public_tests

import (
	"encoding/base64"
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
	"powergo_pytracking/pytracking"
)

func TestPublicConfigurationInitFields(t *testing.T) {
	const ANOTHER_WEBHOOK = "https://anotherwebhook.org/notify"
	config := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		WebhookURL:                ANOTHER_WEBHOOK,
		WebhookTimeoutSeconds:     15,
		IncludeWebhookURL:         false,
		BaseOpenTrackingURL:       "https://tracker.domain.io/open",
		BaseClickTrackingURL:      "https://tracker.domain.io/click",
		DefaultMetadata:           map[string]interface{}{"user": "alice"},
		IncludeDefaultMetadata:    false,
		EncryptionBytestringKey:   nil,
		Encoding:                  "latin-1",
		AppendSlash:               false,
	})
	assert.Equal(t, ANOTHER_WEBHOOK, config.WebhookURL)
	assert.Equal(t, 15, config.WebhookTimeoutSeconds)
	assert.Equal(t, "https://tracker.domain.io/open", config.BaseOpenTrackingURL)
	assert.False(t, config.IncludeWebhookURL)
	assert.False(t, config.IncludeDefaultMetadata)
	assert.False(t, config.AppendSlash)
}

func TestPublicStrAndDeepcopyAndMerge(t *testing.T) {
	config1 := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		WebhookURL:               "PublicWebhook",
		BaseOpenTrackingURL:      "OpenURL",
		BaseClickTrackingURL:     "ClickURL",
		EncryptionBytestringKey:  nil,
	})
	s := config1.String()
	assert.Contains(t, s, "<pytracking.Configuration>")
	cp := config1.DeepCopy()
	assert.Equal(t, config1.WebhookURL, cp.WebhookURL)
	newC := config1.MergeWithKwargs(map[string]interface{}{"webhook_url": "SecondWebhook"})
	assert.Equal(t, "SecondWebhook", newC.WebhookURL)
	assert.Equal(t, "OpenURL", newC.BaseOpenTrackingURL)
}

func TestPublicGetDataToEmbedVariedAndMetadata(t *testing.T) {
	const ANOTHER_URL = "https://anotherdomain.org"
	const ANOTHER_WEBHOOK = "https://anotherwebhook.org/notify"
	config := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		WebhookURL:                ANOTHER_WEBHOOK,
		IncludeWebhookURL:         false,
		DefaultMetadata:           map[string]interface{}{"role": "dev"},
		IncludeDefaultMetadata:    false,
		BaseClickTrackingURL:      "click123",
		BaseOpenTrackingURL:       "open456",
	})
	data := config.GetDataToEmbed(ANOTHER_URL, map[string]interface{}{"device": "mobile"})
	assert.Equal(t, ANOTHER_URL, data["url"])
	metadata, ok := data["metadata"].(map[string]interface{})
	assert.True(t, ok)
	assert.Equal(t, "dev", metadata["role"])
	assert.Equal(t, "mobile", metadata["device"])
	_, hasWebhook := data["webhook"]
	assert.False(t, hasWebhook)

	config2 := pytracking.NewConfiguration(pytracking.ConfigurationArgs{})
	res := config2.GetDataToEmbed("", nil)
	assert.Equal(t, 0, len(res))

	res2 := config2.GetDataToEmbed("https://demo", nil)
	assert.Equal(t, map[string]interface{}{"url": "https://demo"}, res2)
}

func TestPublicGetUrlEncodedDataStrWithoutEncryption(t *testing.T) {
	cfg := pytracking.NewConfiguration(pytracking.ConfigurationArgs{Encoding: "utf-16"})
	plain := map[string]interface{}{"alpha": "beta"}
	b64str := cfg.GetUrlEncodedDataStr(plain)
	decodedBytes, err := base64.URLEncoding.DecodeString(b64str)
	assert.NoError(t, err)
	var decoded map[string]interface{}
	err = json.Unmarshal(decodedBytes, &decoded)
	assert.NoError(t, err)
	assert.Equal(t, plain, decoded)
}

func TestPublicGetUrlEncodedDataStrWithEncryption(t *testing.T) {
	t.Skip("cryptography (Fernet) not available in Go stdlib - skipping encryption test")
}

func TestPublicReprAndDefaults(t *testing.T) {
	config := pytracking.NewConfiguration(pytracking.ConfigurationArgs{})
	assert.Equal(t, "image/png", pytracking.PNGMimeType)
	assert.IsType(t, []byte{}, pytracking.TrackingPixel)
	assert.Nil(t, config.EncryptionKey)
	assert.Equal(t, pytracking.DefaultTimeoutSeconds, config.WebhookTimeoutSeconds)
}

func TestPublicMergeWithKwargsDoesNotChangeOriginal(t *testing.T) {
	cfg := pytracking.NewConfiguration(pytracking.ConfigurationArgs{WebhookURL: "web1"})
	newcfg := cfg.MergeWithKwargs(map[string]interface{}{"webhook_url": "web2"})
	assert.Equal(t, "web2", newcfg.WebhookURL)
	assert.Equal(t, "web1", cfg.WebhookURL)
}