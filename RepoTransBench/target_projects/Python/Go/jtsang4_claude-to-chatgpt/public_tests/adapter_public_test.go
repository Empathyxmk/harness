package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type DummyClaudeAdapter struct {
	claudeApiKey string
	url string
}

func (ca *DummyClaudeAdapter) GetApiKey(headers map[string]string) string {
	auth, ok := headers["authorization"]
	if ok && len(auth) > 7 && auth[:7] == "Bearer " {
		return auth[7:]
	}
	return ca.claudeApiKey
}
func (ca *DummyClaudeAdapter) ConvertMessagesToPrompt(messages []map[string]string) string {
	prompt := ""
	for _, m := range messages {
		role := m["role"]
		content := m["content"]
		if role == "user" || role == "system" {
			prompt += "\n\nHuman: " + content
		} else if role == "assistant" {
			prompt += "\n\nAssistant: " + content
		}
	}
	prompt += "\n\nAssistant: "
	return prompt
}
func (ca *DummyClaudeAdapter) OpenAIToClaudeParams(oai map[string]interface{}) map[string]interface{} {
	model, ok := oai["model"].(string)
	if !ok || model != "gpt-4-0314" {
		model = "claude-2"
	}
	prompt := "DIFFERENT_PROMPT"
	if f, ok := ca.(interface{ ConvertMessagesToPrompt([]map[string]string) string }); ok {
		prompt = f.ConvertMessagesToPrompt(nil)
	}
	params := map[string]interface{}{
		"model": model,
		"prompt": prompt,
		"max_tokens_to_sample": 100000,
	}
	if v, ok := oai["max_tokens"]; ok {
		params["max_tokens_to_sample"] = v
	}
	if v, ok := oai["stop"]; ok {
		params["stop_sequences"] = v
	}
	if v, ok := oai["temperature"]; ok {
		params["temperature"] = v
	}
	if v, ok := oai["stream"]; ok {
		params["stream"] = v
	}
	return params
}

func TestGetApiKeyFromHeadersPublic(t *testing.T) {
	ca := &DummyClaudeAdapter{url: "http://another-url", claudeApiKey: ""}
	headers := map[string]string{"authorization": "Bearer another-key"}
	assert.Equal(t, "another-key", ca.GetApiKey(headers))

	ca.claudeApiKey = "second-env-key"
	assert.Equal(t, "second-env-key", ca.GetApiKey(map[string]string{}))
}

func TestConvertMessagesToPromptRolesPublic(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	messages := []map[string]string{
		{"role": "user", "content": "How are you?"},
		{"role": "assistant", "content": "I'm fine, thank you."},
		{"role": "system", "content": "System message here"},
	}
	prompt := ca.ConvertMessagesToPrompt(messages)
	assert.Contains(t, prompt, "\n\nHuman: How are you?")
	assert.Contains(t, prompt, "\n\nAssistant: I'm fine, thank you.")
	assert.Contains(t, prompt, "\n\nHuman: How are you?")
	assert.True(t, len(prompt) >= 10 && prompt[len(prompt)-10:] == "Assistant: ")
}

func TestOpenAIToClaudeParamsAllPublic(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	oai := map[string]interface{}{
		"model": "gpt-4-0314",
		"messages": []map[string]string{},
		"max_tokens": 1024,
		"stop": []string{"STOP_NOW"},
		"temperature": 0.55,
		"stream": false,
	}
	result := ca.OpenAIToClaudeParams(oai)
	assert.Equal(t, "gpt-4-0314", result["model"])
	assert.Equal(t, "DIFFERENT_PROMPT", result["prompt"])
	assert.Equal(t, 1024, result["max_tokens_to_sample"])
	assert.Equal(t, []string{"STOP_NOW"}, result["stop_sequences"])
	assert.Equal(t, 0.55, result["temperature"])
	assert.Equal(t, false, result["stream"])
}

func TestOpenAIToClaudeParamsPartialPublic(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	oai := map[string]interface{}{
		"model": "absent-model",
		"messages": []map[string]string{},
	}
	result := ca.OpenAIToClaudeParams(oai)
	assert.Equal(t, "claude-2", result["model"])
	assert.Equal(t, "DIFFERENT_PROMPT", result["prompt"])
	assert.Equal(t, 100000, result["max_tokens_to_sample"])
}

func TestConvertMessagesToPromptCorrectFormatPublic(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	messages := []map[string]string{
		{"role": "user", "content": "What's up?"},
	}
	result := ca.ConvertMessagesToPrompt(messages)
	assert.True(t, len(result) >= 25 && result[:20] == "\n\nHuman: What's up?" && result[len(result)-11:] == "Assistant: ")
}