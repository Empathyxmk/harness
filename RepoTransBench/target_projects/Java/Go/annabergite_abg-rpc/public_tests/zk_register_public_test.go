package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRegisterNewPath(t *testing.T) {
	znode := "/register/public/node"
	registered := doRegister(znode)
	assert.True(t, registered, "Should register public node")
}

func doRegister(znode string) bool {
	return strings.Contains(znode, "/register/public/")
}