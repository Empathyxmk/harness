package original

import (
	"strings"
	"testing"

	"github.com/example/flasklogin/src"
)

func TestAboutWarns(t *testing.T) {
	msg := src.AboutWarn()
	if !strings.Contains(strings.ToLower(msg), "deprecated") {
		t.Errorf("AboutWarn did not warn about deprecation")
	}
	if src.__title__ != "Flask-Login" {
		t.Errorf("Expected __title__ to be 'Flask-Login'")
	}
	if src.__version__ != "0.7.0" {
		t.Errorf("Expected __version__ to be '0.7.0'")
	}
}

func TestInitDunderVersionWarns(t *testing.T) {
	returned, warn := src.DunderVersion(func(string) string { return "1.2.3" })
	if returned != "1.2.3" {
		t.Errorf("Expected DunderVersion to return '1.2.3'")
	}
	if !strings.Contains(strings.ToLower(warn), "deprecated") {
		t.Errorf("Expected a deprecation warning")
	}
}

func TestInitDunderVersionAttributeError(t *testing.T) {
	err := src.DunderVersionAttributeError("notarealattr")
	if err == nil || err.Error() != "notarealattr" {
		t.Errorf("Expected AttributeError with message 'notarealattr'")
	}
}