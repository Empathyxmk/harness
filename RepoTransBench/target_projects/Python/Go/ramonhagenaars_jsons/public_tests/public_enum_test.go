package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

type PublicTestEnum int

const (
	ALPHA PublicTestEnum = 9
	BETA  PublicTestEnum = 16
)

func (e PublicTestEnum) String() string {
	switch e {
	case ALPHA:
		return "ALPHA"
	case BETA:
		return "BETA"
	}
	return ""
}

func TestEnumDumpsName(t *testing.T) {
	result := jsons.Dumps(ALPHA)
	assert.Equal(t, `"ALPHA"`, result)
}

func TestEnumLoadsName(t *testing.T) {
	val := jsons.LoadEnum("BETA", ALPHA)
	assert.Equal(t, BETA, val)
}

func TestEnumDumpAndLoadName(t *testing.T) {
	result := jsons.Dumps(BETA)
	loaded := jsons.LoadEnum("BETA", ALPHA)
	assert.Equal(t, `"BETA"`, result)
	assert.Equal(t, BETA, loaded)
}