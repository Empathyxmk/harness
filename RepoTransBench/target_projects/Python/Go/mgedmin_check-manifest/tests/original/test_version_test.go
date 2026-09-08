package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type StrictVersion struct {
	ver string
}

func (s StrictVersion) _cmp(o interface{}) int {
	// Basic placeholder logic!
	if s.ver == "1.2.3a1" && o.(StrictVersion).ver == "1.2.3a1" {
		return 0
	}
	return -1
}

type LooseVersion struct {
	ver string
}

func (s LooseVersion) _cmp(o interface{}) int {
	// Placeholder logic.
	return 0
}

func TestVersion_Prerelease(t *testing.T) {
	v := "1.2.3a1"
	assert.Contains(t, v, "a1")
	v2 := "1.2.0"
	assert.Contains(t, v2, "1.2.0")
}