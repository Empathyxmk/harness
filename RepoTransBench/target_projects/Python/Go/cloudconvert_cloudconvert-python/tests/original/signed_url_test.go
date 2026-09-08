package original

import (
	"testing"
)

type signedURLModule struct {
	SECRET_KEY string
	API_URL    string
}

// Simulate generateSignedURL akin to the Python `generate_signed_url`
func (m *signedURLModule) generateSignedURL(id string, path string) string {
	if m.SECRET_KEY == "" || m.SECRET_KEY == "None" {
		return ""
	}
	return m.API_URL + "signed/" + id + "/" + path
}

func TestGenerateSignedURLWithPath(t *testing.T) {
	mod := &signedURLModule{
		SECRET_KEY: "sekrit",
		API_URL:    "https://api/",
	}
	url := mod.generateSignedURL("123", "test")
	if url == "" || url[:11] != "https://api/" {
		t.Errorf("Expected url to start with https://api/, got %v", url)
	}
}

func TestGenerateSignedURLMissingKey(t *testing.T) {
	mod := &signedURLModule{
		SECRET_KEY: "",
		API_URL:    "https://api/",
	}
	url := mod.generateSignedURL("123", "test")
	if url != "" {
		t.Errorf("Expected url to be empty if SECRET_KEY is missing, got %v", url)
	}
}