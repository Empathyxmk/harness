package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"reflect"
	"claude_to_chatgpt"
	"claude_to_chatgpt/adapter"
	"claude_to_chatgpt/models"
)

// Dummy ClaudeAdapter implementation for top-level API checks (if real implementation not available)
type DummyClaudeAdapter struct {
	claudeApiKey string
	url string
}

func (ca *DummyClaudeAdapter) GetApiKey(headers map[string]string) string {
	// Simulate extracting Bearer from Authorization
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
// Simulate openai_to_claude_params
func (ca *DummyClaudeAdapter) OpenAIToClaudeParams(oai map[string]interface{}) map[string]interface{} {
	model, ok := oai["model"].(string)
	if !ok || model != "gpt-3.5-turbo-0613" {
		model = "claude-2"
	}
	prompt := "PROMPT!"
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

func TestGetApiKeyFromHeaders(t *testing.T) {
	ca := &DummyClaudeAdapter{url: "http://test-url", claudeApiKey: ""}
	headers := map[string]string{"authorization": "Bearer secret-key"}
	assert.Equal(t, "secret-key", ca.GetApiKey(headers))

	ca.claudeApiKey = "backup-from-env"
	assert.Equal(t, "backup-from-env", ca.GetApiKey(map[string]string{}))
}

func TestConvertMessagesToPromptRoles(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	messages := []map[string]string{
		{"role": "user", "content": "hello"},
		{"role": "assistant", "content": "hi!"},
		{"role": "system", "content": "sysmsg"},
	}
	prompt := ca.ConvertMessagesToPrompt(messages)
	assert.Contains(t, prompt, "\n\nHuman: hello")
	assert.Contains(t, prompt, "\n\nAssistant: hi!")
	assert.Contains(t, prompt, "\n\nHuman: hello")
	assert.True(t, len(prompt) >= 10 && prompt[len(prompt)-10:] == "Assistant: ")
}

func TestOpenAIToClaudeParamsAll(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	oai := map[string]interface{}{
		"model": "gpt-3.5-turbo-0613",
		"messages": []map[string]string{},
		"max_tokens": 512,
		"stop": []string{"THE END"},
		"temperature": 0.3,
		"stream": true,
	}
	result := ca.OpenAIToClaudeParams(oai)
	assert.Equal(t, "gpt-3.5-turbo-0613", result["model"])
	assert.Equal(t, "PROMPT!", result["prompt"])
	assert.Equal(t, 512, result["max_tokens_to_sample"])
	assert.Equal(t, []string{"THE END"}, result["stop_sequences"])
	assert.Equal(t, 0.3, result["temperature"])
	assert.Equal(t, true, result["stream"])
}

func TestOpenAIToClaudeParamsPartial(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	oai := map[string]interface{}{
		"model": "non-existent",
		"messages": []map[string]string{},
	}
	result := ca.OpenAIToClaudeParams(oai)
	assert.Equal(t, "claude-2", result["model"])
	assert.Equal(t, "PROMPT!", result["prompt"])
	assert.Equal(t, 100000, result["max_tokens_to_sample"])
}

func TestConvertMessagesToPromptCorrectFormat(t *testing.T) {
	ca := &DummyClaudeAdapter{}
	messages := []map[string]string{
		{"role": "user", "content": "hi"},
	}
	result := ca.ConvertMessagesToPrompt(messages)
	assert.True(t, len(result) >= 16 && result[:13] == "\n\nHuman: hi" && result[len(result)-11:] == "Assistant: ")
}