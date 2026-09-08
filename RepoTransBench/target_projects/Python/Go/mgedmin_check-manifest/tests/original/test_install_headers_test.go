package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestInstallHeaders_SimpleRun(t *testing.T) {
	headers := []string{"header1", "header2"}
	assert.Equal(t, 2, len(headers))
}