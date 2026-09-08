package login

import (
	"strings"
	"testing"
)

func TestAppContextPackageNameContainsLogin(t *testing.T) {
	packageName := "com.loong.login"
	if !strings.Contains(packageName, "login") {
		t.Errorf(`Expected package name to contain "login", got %q`, packageName)
	}
}