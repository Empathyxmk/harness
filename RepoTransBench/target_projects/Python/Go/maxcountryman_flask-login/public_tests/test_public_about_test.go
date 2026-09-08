package public_tests

import (
	"strings"
	"testing"

	"github.com/example/flasklogin/src"
)

func TestAboutWarnsPublic(t *testing.T) {
	msg := src.AboutWarn()
	if !strings.Contains(strings.ToLower(msg), "deprecated") {
		t.Errorf("Deprecation warning missing")
	}
	if !strings.Contains(src.__title__, "Flask") {
		t.Errorf("__title__ does not contain 'Flask'")
	}
	if len(strings.Split(src.__version__, ".")) != 3 {
		t.Errorf("__version__ not version-like")
	}
}

func TestInitDunderVersionWarnsPublic(t *testing.T) {
	val, warn := src.DunderVersion(func(string) string { return "2.0.1" })
	if val != "2.0.1" {
		t.Errorf("Expected version '2.0.1'")
	}
	if !strings.Contains(strings.ToLower(warn), "deprecated") {
		t.Errorf("Expected a deprecation warning")
	}
}

func TestInitDunderVersionAttributeErrorPublic(t *testing.T) {
	attr := "certainlynotanattribute"
	err := src.DunderVersionAttributeError(attr)
	if err == nil || err.Error() != attr {
		t.Errorf("Expected AttributeError with message %s", attr)
	}
}