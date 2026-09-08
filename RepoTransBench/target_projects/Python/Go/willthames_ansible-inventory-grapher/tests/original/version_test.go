package original

import (
	"testing"
)

var versionString = "1.2.3"

func TestVersionString(t *testing.T) {
	if _, ok := interface{}(versionString).(string); !ok {
		t.Errorf("version is not string")
	}
	if len(versionString) < 3 || versionString[1] != '.' {
		t.Errorf("version does not contain dot: %q", versionString)
	}
}