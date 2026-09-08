package public_tests

import "testing"

var (
	API_URL    = "https://public-api/"
	SECRET_KEY = "abc"
)

func TestConfigImportsPublic(t *testing.T) {
	if API_URL == "" && SECRET_KEY == "" {
		t.Errorf("Expected at least API_URL or SECRET_KEY to be defined")
	}
}