package public_tests

import (
	"testing"
	"github.com/jarcoal/httpmock"
	"github.com/stretchr/testify/assert"
)

// minimal Channels struct stub for testing; use your real struct when available
type Channels struct {
	Token string
}

func (c *Channels) GetChannelID(name string) string {
	resp, _ := httpmock.Get("https://slack.com/api/channels.list")
	channels := struct {
		Ok       string `json:"ok"`
		Channels []struct {
			Name string `json:"name"`
			ID   string `json:"id"`
		} `json:"channels"`
	}{}
	_ = json.Unmarshal([]byte(resp.Body), &channels)
	for _, ch := range channels.Channels {
		if ch.Name == name {
			return ch.ID
		}
	}
	return ""
}

func TestChannelsPublic_ValidIDsReturnChannelID(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	response := `{
		"ok": "true",
		"channels": [
			{"name": "dev", "id": "C333"},
			{"name": "support", "id": "C444"}
		]
	}`
	httpmock.RegisterResponder(
		"GET",
		"https://slack.com/api/channels.list",
		httpmock.NewStringResponder(200, response),
	)
	channels := Channels{Token: "public_token"}
	id := channels.GetChannelID("support")
	assert.Equal(t, "C444", id)
}

func TestChannelsPublic_InvalidChannelIDsReturnNone(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	response := `{
		"ok": "true",
		"channels": [
			{"name": "dev", "id": "C333"},
			{"name": "support", "id": "C444"}
		]
	}`
	httpmock.RegisterResponder(
		"GET",
		"https://slack.com/api/channels.list",
		httpmock.NewStringResponder(200, response),
	)
	channels := Channels{Token: "public_token"}
	id := channels.GetChannelID("not_a_channel")
	assert.Equal(t, "", id)
}