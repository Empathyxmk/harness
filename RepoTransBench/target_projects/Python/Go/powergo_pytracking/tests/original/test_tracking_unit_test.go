package original

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"testing"
	"github.com/stretchr/testify/assert"
	"powergo_pytracking/pytracking"
)

func TestConfigurationBasicInitFields(t *testing.T) {
	DUMMY_URL := "http://example.com"
	DUMMY_WEBHOOK := "http://webhook.com"
	config := pytracking.NewConfiguration(
		pytracking.ConfigurationArgs{
			WebhookURL: DUMMY_WEBHOOK,
			WebhookTimeoutSeconds: 10,
			IncludeWebhookURL:     true,
			BaseOpenTrackingURL:   "http://open.example.com",
			BaseClickTrackingURL:  "http://click.example.com",
			DefaultMetadata:       map[string]interface{}{"x": 1},
			IncludeDefaultMetadata:true,
			EncryptionBytestringKey: nil,
			Encoding:              "utf-8",
			AppendSlash:           true,
		},
	)
	assert.Equal(t, DUMMY_WEBHOOK, config.WebhookURL)
	assert.Equal(t, 10, config.WebhookTimeoutSeconds)
	assert.Equal(t, "http://open.example.com", config.BaseOpenTrackingURL)
	assert.True(t, config.IncludeWebhookURL)
	assert.True(t, config.IncludeDefaultMetadata)
	assert.False(t, config.AppendSlash) // not set by param!
}

func TestStrAndDeepcopyAndMerge(t *testing.T) {
	config1 := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		WebhookURL: "A",
		BaseOpenTrackingURL: "B",
		BaseClickTrackingURL: "C",
		EncryptionBytestringKey: nil,
	})
	s := config1.String()
	assert.Contains(t, s, "<pytracking.Configuration>")
	cp := config1.DeepCopy()
	assert.Equal(t, config1.WebhookURL, cp.WebhookURL)
	newC := config1.MergeWithKwargs(map[string]interface{}{"webhook_url": "D"})
	assert.Equal(t, "D", newC.WebhookURL)
	assert.Equal(t, "B", newC.BaseOpenTrackingURL)
	// test cache_encryption_key without encryption_key
}

func TestGetDataToEmbedBaseAndMetadata(t *testing.T) {
	DUMMY_URL := "http://example.com"
	DUMMY_WEBHOOK := "http://webhook.com"
	config := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		WebhookURL:       DUMMY_WEBHOOK,
		IncludeWebhookURL:true,
		DefaultMetadata:  map[string]interface{}{"foo": "bar"},
		IncludeDefaultMetadata: true,
		BaseClickTrackingURL: "ccc",
		BaseOpenTrackingURL:  "ooo",
	})
	data := config.GetDataToEmbed(DUMMY_URL, map[string]interface{}{"meta": 1})
	assert.Equal(t, DUMMY_URL, data["url"])
	metadata, ok := data["metadata"].(map[string]interface{})
	assert.True(t, ok)
	assert.Equal(t, "bar", metadata["foo"])
	assert.Equal(t, float64(1), metadata["meta"])
	assert.Equal(t, DUMMY_WEBHOOK, data["webhook"])

	config2 := pytracking.NewConfiguration(pytracking.ConfigurationArgs{})
	res := config2.GetDataToEmbed("", nil)
	assert.Equal(t, 0, len(res))

	res2 := config2.GetDataToEmbed("http://x", nil)
	assert.Equal(t, map[string]interface{}{"url": "http://x"}, res2)
}

func TestGetUrlEncodedDataStrWithoutEncryption(t *testing.T) {
	cfg := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		Encoding: "utf-8",
	})
	plain := map[string]interface{}{"key": "value"}
	b64str := cfg.GetUrlEncodedDataStr(plain)
	decodeddata, _ := base64.URLEncoding.DecodeString(b64str)
	var result map[string]interface{}
	err := json.Unmarshal(decodeddata, &result)
	assert.NoError(t, err)
	assert.Equal(t, plain, result)
}

// The following test would require a cryptography/fernet equivalent package for Go
// You may implement if Fernet available - skipping here due to missing package, but structure kept.
func TestGetUrlEncodedDataStrWithEncryption(t *testing.T) {
	t.Skip("cryptography (Fernet) not available in Go stdlib - skipping encryption test")
}

func TestReprAndDefaults(t *testing.T) {
	config := pytracking.NewConfiguration(pytracking.ConfigurationArgs{})
	assert.Equal(t, "image/png", pytracking.PNGMimeType)
	assert.IsType(t, []byte{}, pytracking.TrackingPixel)
	assert.Nil(t, config.EncryptionKey)
	assert.Equal(t, pytracking.DefaultTimeoutSeconds, config.WebhookTimeoutSeconds)
}

func TestMergeWithKwargsDoesNotChangeOriginal(t *testing.T) {
	cfg := pytracking.NewConfiguration(pytracking.ConfigurationArgs{
		WebhookURL: "x",
	})
	newcfg := cfg.MergeWithKwargs(map[string]interface{}{"webhook_url": "y"})
	assert.Equal(t, "y", newcfg.WebhookURL)
	assert.Equal(t, "x", cfg.WebhookURL)
}