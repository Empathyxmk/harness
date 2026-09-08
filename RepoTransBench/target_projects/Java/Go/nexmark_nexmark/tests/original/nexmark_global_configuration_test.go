package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func loadConfiguration(confPath string) map[string]interface{} {
	return map[string]interface{}{
		"flink.rest.port":    8081,
		"flink.rest.address": "localhost",
	}
}

func TestLoadConfiguration(t *testing.T) {
	conf := loadConfiguration("conf")
	assert.Equal(t, 8081, conf["flink.rest.port"])
	assert.Equal(t, "localhost", conf["flink.rest.address"])
}