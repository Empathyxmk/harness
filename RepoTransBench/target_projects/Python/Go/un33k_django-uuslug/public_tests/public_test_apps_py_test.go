package public_tests

import (
	"strings"
	"testing"
)

type UuslugConfig struct {
	Name        string
	VerboseName string
}

func TestAppsConfigNamePublic(t *testing.T) {
	appConfig := UuslugConfig{Name: "uuslug", VerboseName: "Uuslug App"}
	if appConfig.Name != "uuslug" {
		t.Errorf("Expected appConfig.Name to be 'uuslug', got %s", appConfig.Name)
	}
	if appConfig.VerboseName == "" {
		t.Error("Expected VerboseName to be present")
	}
	if !strings.Contains(strings.ToLower(appConfig.VerboseName), "uuslug") {
		t.Error("Expected verbose_name to contain 'uuslug'")
	}
}