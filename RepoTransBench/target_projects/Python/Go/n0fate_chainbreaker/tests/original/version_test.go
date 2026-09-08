package original

import (
	"strings"
	"testing"
)

var version = "1.0.0"

func TestVersionStr(t *testing.T) {
	if reflect.TypeOf(version).Kind() != reflect.String {
		t.Errorf("Expected version to be string")
	}
	if strings.Count(version, ".") < 1 {
		t.Errorf("Version string should contain at least one dot")
	}
}