package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestYsoConfigSmoke_DefaultConfig(t *testing.T) {
	conf := yso.NewYsoConfig()
	assert.NotNil(t, conf)
	assert.NotNil(t, conf.GetConfig())
}

func TestYsoConfigSmoke_SetAndGetConfig(t *testing.T) {
	conf := yso.NewYsoConfig()
	props := make(map[string]string)
	props["foo"] = "bar"
	conf.SetConfig(props)
	assert.Equal(t, "bar", conf.GetConfig()["foo"])
}

func TestYsoConfigSmoke_ToString(t *testing.T) {
	conf := yso.NewYsoConfig()
	conf.GetConfig()["k"] = "v"
	str := conf.String()
	assert.Contains(t, str, "k")
	assert.Contains(t, str, "v")
}