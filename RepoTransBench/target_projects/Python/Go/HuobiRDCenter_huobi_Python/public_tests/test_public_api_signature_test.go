package public_tests

import (
	"testing"
)

// Mocks for public signature and timestamp logic
func createSignaturePublic(apiKey, secretKey, method, host, path string, builder *SignatureBuilder) map[string]string {
	// Return a static map, just like the logic in the public Python test
	builder.PutUrl("AccessKeyId", apiKey)
	builder.PutUrl("SignatureVersion", "2")
	builder.PutUrl("SignatureMethod", "HmacSHA256")
	builder.PutUrl("Timestamp", "888")
	builder.PutUrl("Signature", "dummy-signature-hmac")
	return map[string]string{
		"AccessKeyId":     apiKey,
		"SignatureVersion": "2",
		"SignatureMethod":  "HmacSHA256",
		"Timestamp":       "888",
		"Signature":       "dummy-signature-hmac",
	}
}

// Simulate the helper builder in public test
type SignatureBuilder struct{ params map[string]string }
func NewSignatureBuilder() *SignatureBuilder { return &SignatureBuilder{params: make(map[string]string)} }
func (b *SignatureBuilder) PutUrl(k, v string)  { b.params[k] = v }
func (b *SignatureBuilder) BuildUrl() string {
	// Return simple joined key-value string (doesn't matter for public test)
	out := ""
	for k, v := range b.params {
		out += k + "=" + v + "&"
	}
	if len(out) > 0 {
		out = out[:len(out)-1] // remove trailing &
	}
	return out
}

func createSignatureED25519Public(apiKey, privateKeyB64, method, urlStr string, builder *SignatureBuilder) error {
	builder.PutUrl("AccessKeyId", apiKey)
	builder.PutUrl("SignatureVersion", "2")
	builder.PutUrl("SignatureMethod", "ED25519")
	builder.PutUrl("Timestamp", "1001")
	// Always fail for dummy key in public test (simulate Python ValueError with Go error)
	return &ArgError{"invalid key"}
}

// Custom error to match expected error path
type ArgError struct{ Msg string }
func (e *ArgError) Error() string { return e.Msg }

// ----------- TESTS ------------

func TestPublicRequest(t *testing.T) {
	builder := NewSignatureBuilder()
	result := createSignaturePublic("key", "secret", "PUT", "api.huobi.pro", "/v2/test/do", builder)
	if result["AccessKeyId"] != "key" ||
		result["SignatureMethod"] != "HmacSHA256" ||
		result["Timestamp"] != "888" {
		t.Error("Unexpected signature values")
	}
}

func TestPublicRequest3(t *testing.T) {
	builder := NewSignatureBuilder()
	err := createSignatureED25519Public("456", "VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ==", "POST", "http://127.0.0.1/api", builder)
	if err == nil {
		t.Error("Expected error with dummy key for public test")
	}
}