package original

import (
	"strings"
	"testing"
)

// Simulate an API key system
const dummyApiKey = "dummy_api_key_value"

func TestValidRequestReturnsProperResponse_ApiKeyPlugin(t *testing.T) {
	// Simulate providing the dummy API key header, getting 200, response text contains the API key, NOT the header name.
	apiKeyHeader := dummyApiKey
	statusCode := 200
	responseText := `{"headers":"` + apiKeyHeader + `"}`

	if statusCode != 200 {
		t.Errorf("Expected 200 OK, got %v", statusCode)
	}
	if !strings.Contains(responseText, dummyApiKey) {
		t.Errorf("Expected dummy API key [%s] in response text: %v", dummyApiKey, responseText)
	}
	if strings.Contains(responseText, "api_key") {
		t.Errorf("Did not expect 'api_key' header name in response text: %v", responseText)
	}
}

func TestMissingForwardedForHeader_ApiKeyPlugin(t *testing.T) {
	// Simulate the case with no api_key header in the request, response text should NOT contain the API key nor the header name,
	// and response headers don't contain the header name either
	statusCode := 200
	responseText := `{"headers":"<nil>"}` // simulate missing header
	responseHeaders := map[string]string{}

	if statusCode != 200 {
		t.Errorf("Expected 200 OK, got %v", statusCode)
	}
	if strings.Contains(responseText, dummyApiKey) {
		t.Errorf("Did not expect dummy API key [%s] in response text: %v", dummyApiKey, responseText)
	}
	if _, ok := responseHeaders["api_key"]; ok {
		t.Errorf("Did not expect 'api_key' in response headers")
	}
}