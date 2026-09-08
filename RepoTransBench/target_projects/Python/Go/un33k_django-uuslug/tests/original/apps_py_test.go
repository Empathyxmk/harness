package original

import (
	"testing"
)

type AppConfig struct {
	Label       string
	VerboseName string
}

func TestAppsModuleImport(t *testing.T) {
	app := AppConfig{Label: "uuslug", VerboseName: "Uuslug"}
	if app.Label != "uuslug" && app.VerboseName == "" {
		t.Error("AppConfig missing expected attributes")
	}
}

func TestAppsModuleSmoke(t *testing.T) {
	app := AppConfig{Label: "uuslug", VerboseName: "Uuslug"}
	if app.VerboseName == "" {
		t.Error("AppConfig.VerboseName missing")
	}
}