package public_tests

import (
	"testing"

	"yinjihuan_netty_im_go/tests"
	"github.com/stretchr/testify/assert"
)

func TestServerPoHandlerConstructionPublic(t *testing.T) {
	handler := tests.NewServerPoHandler()
	assert.NotNil(t, handler)
	assert.Equal(t, "ServerPoHandler", handler.ClassName())
}

func TestServerPoHandlerProtoConstructionPublic(t *testing.T) {
	handlerProto := tests.NewServerPoHandlerProto()
	assert.NotNil(t, handlerProto)
	assert.Contains(t, handlerProto.ClassName(), "Proto")
}

func TestServerStringHandlerConstructionPublic(t *testing.T) {
	stringHandler := tests.NewServerStringHandler()
	assert.NotNil(t, stringHandler)
	assert.Contains(t, stringHandler.ClassName(), "String")
}