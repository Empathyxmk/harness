package public_tests

import (
	"testing"

	"yinjihuan_netty_im_go/tests"
	"github.com/stretchr/testify/assert"
)

func TestImServerConstructorPublic(t *testing.T) {
	server := tests.NewImServer()
	assert.Equal(t, "ImServer", server.ClassName())
}