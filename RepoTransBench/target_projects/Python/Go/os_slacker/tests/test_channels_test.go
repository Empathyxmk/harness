package tests

import (
	"testing"
	"github.com/jarcoal/httpmock"
	"github.com/stretchr/testify/assert"
	"os_slacker/slacker"
	"os_slacker/slacker/utilities"
)

// Mocks and basic struct definitions for the translated tests

// Minimal Channels struct to make tests compilable; replace with the actual implementation
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

func TestValidIDsReturnChannelID(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()

	response := `{
		"ok": "true",
		"channels": [
			{"name": "general", "id": "C111"},
			{"name": "random", "id": "C222"}
		]
	}`

	httpmock.RegisterResponder(
		"GET",
		utilities.GetAPIURL("channels.list"),
		httpmock.NewStringResponder(200, response),
	)

	channels := Channels{Token: "aaa"}
	channelID := channels.GetChannelID("general")
	assert.Equal(t, "C111", channelID)
}

func TestInvalidChannelIDsReturnNone(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()

	response := `{
		"ok": "true",
		"channels": [
			{"name": "general", "id": "C111"},
			{"name": "random", "id": "C222"}
		]
	}`

	httpmock.RegisterResponder(
		"GET",
		utilities.GetAPIURL("channels.list"),
		httpmock.NewStringResponder(200, response),
	)

	channels := Channels{Token: "aaa"}
	channelID := channels.GetChannelID("fake_group")
	assert.Equal(t, "", channelID)
}