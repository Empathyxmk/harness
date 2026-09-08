package public_tests

import (
	"testing"
	"bumpversion"
)

func TestConfigFileSectionDefaults(t *testing.T) {
	conf := map[string]interface{}{"current_version": "2.2.2", "parse": "abc(?P<alpha>[a-zA-Z]+)", "serialize": []string{"{alpha}"}}
	options := bumpversion.NewConfiguredFile("setup.cfg", conf, map[string]interface{}{})
	serialize, ok := options.Serialize().([]string)
	if !ok || len(serialize) != 1 || serialize[0] != "{alpha}" {
		t.Errorf("Expected serialize == [\"{alpha}\"], got %v", serialize)
	}
}

func TestDefaultParsePatternIsUsedNew(t *testing.T) {
	conf := map[string]interface{}{"current_version": "1.9.9"}
	options := bumpversion.NewConfiguredFile("pyproject.toml", conf, map[string]interface{}{})
	if options.ConfigFile() != "pyproject.toml" {
		t.Errorf("Expected ConfigFile() == \"pyproject.toml\"")
	}
}