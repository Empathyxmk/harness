package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestVersion(t *testing.T) {
	ver := jsons.Version()
	spl := strings.Split(ver, ".")
	assert.Equal(t, 3, len(spl))
}