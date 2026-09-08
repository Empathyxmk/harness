package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyConfigAuth struct {
	API_ROOT string
	AUTH     string
}

func apiConfigurationAuth() DummyConfigAuth {
	return DummyConfigAuth{API_ROOT: "http://testing", AUTH: "FlaskForwardAuth"}
}

func validResponseAuth() map[string]interface{} {
	return make(map[string]interface{})
}

func TestFlaskAuthForward(t *testing.T) {
	config := apiConfigurationAuth()
	header := "Bearer 11111111-1111-1111-1111-111111111111"
	assert.Equal(t, "FlaskForwardAuth", config.AUTH)
	assert.Equal(t, "http://testing", config.API_ROOT)
	assert.Contains(t, header, "Bearer")
}