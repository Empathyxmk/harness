package public_tests

import (
	"testing"
)

type signedURLModulePublic struct {
	SECRET_KEY string
	API_URL    string
}

func (m *signedURLModulePublic) generateSignedURL(id string, path string) string {
	if m.SECRET_KEY == "" {
		return ""
	}
	return m.API_URL + "signed/" + id + "/" + path
}

func TestGenerateSignedURLWithPathPublic(t *testing.T) {
	mod := &signedURLModulePublic{
		SECRET_KEY: "public123",
		API_URL:    "https://public-api/",
	}
	url := mod.generateSignedURL("999", "sample")
	if url == "" || url[:19] != "https://public-api/" {
		t.Errorf("Expected url starting https://public-api/, got %v", url)
	}
}

func TestGenerateSignedURLMissingKeyPublic(t *testing.T) {
	mod := &signedURLModulePublic{
		SECRET_KEY: "",
		API_URL:    "https://public-api/",
	}
	url := mod.generateSignedURL("456", "demo")
	if url != "" {
		t.Errorf("Expected url to be empty when SECRET_KEY is missing, got %v", url)
	}
}