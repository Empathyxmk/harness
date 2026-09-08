package original

import (
	"testing"
)

func TestVersion(t *testing.T) {
	version := "1.2.3"
	if len(version) == 0 {
		t.Error("version string is empty")
	}
}