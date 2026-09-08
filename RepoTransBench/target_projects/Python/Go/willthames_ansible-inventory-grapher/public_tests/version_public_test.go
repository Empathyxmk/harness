package public_tests

import (
	"strings"
	"testing"
)

const publicVersionString = "2.3.4"

func TestPublicVersionString(t *testing.T) {
	if _, ok := interface{}(publicVersionString).(string); !ok {
		t.Error("public version is not string")
	}
	if cnt := strings.Count(publicVersionString, "."); cnt != 2 {
		t.Errorf("public version string has unexpected number of dots: %d", cnt)
	}
}