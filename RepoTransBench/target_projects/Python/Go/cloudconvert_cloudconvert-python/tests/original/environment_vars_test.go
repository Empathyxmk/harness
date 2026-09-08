package original

import (
	"testing"
)

const (
	CLOUDCONVERT_API_KEY = "API_KEY"
	CLOUDCONVERT_SANDBOX = "true"
)

var ModuleDoc = "Environment Variables for Cloudconvert Go library"

func TestEnvVarsNames(t *testing.T) {
	if CLOUDCONVERT_API_KEY != "API_KEY" {
		t.Errorf("CLOUDCONVERT_API_KEY should be API_KEY")
	}
	if CLOUDCONVERT_SANDBOX != "true" {
		t.Errorf("CLOUDCONVERT_SANDBOX should be true")
	}
}

func TestEnvModuleStrings(t *testing.T) {
	if ModuleDoc == "" || ModuleDoc == "None" {
		t.Errorf("Environment Variables docstring missing from module")
	}
}