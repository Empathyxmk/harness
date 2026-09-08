package public_tests

import "testing"

const (
	SOME_PUBLIC_API_KEY = "keypublic123"
)

func TestEnvironmentImportPublic(t *testing.T) {
	if SOME_PUBLIC_API_KEY == "" {
		t.Errorf("SOME_PUBLIC_API_KEY should be set")
	}
}

func TestEnvVarNotSetPublic(t *testing.T) {
	var apiKey string // intentionally unset
	if apiKey != "" {
		t.Errorf("apiKey should be empty by default")
	}
}