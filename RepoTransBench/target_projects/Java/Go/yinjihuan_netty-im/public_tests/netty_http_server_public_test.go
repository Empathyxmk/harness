package public_tests

import (
	"testing"
	"yinjihuan_netty_im_go/tests"
	"github.com/stretchr/testify/assert"
)

func TestServerInstantiationPublic(t *testing.T) {
	server := tests.NewNettyHttpServer()
	assert.NotNil(t, server)
	assert.Contains(t, server.ClassName(), "NettyHttpServer")
}

func TestHandlerInstantiationPublic(t *testing.T) {
	handler := tests.NewNettyHttpServerHandler()
	assert.NotNil(t, handler)
	assert.Contains(t, handler.ClassName(), "Handler")
}