package original

import (
	"strings"
	"testing"
	"github.com/stretchr/testify/assert"
	"zfkun_ja_netfilter_mymap_plugin/tests"
)

func TestInitAndGetters(t *testing.T) {
	entry := tests.NewMyPluginEntry()
	entry.Init(nil, &tests.PluginConfig{})
	assert.NotNil(t, entry.GetTransformers())
}

func TestMeta(t *testing.T) {
	entry := tests.NewMyPluginEntry()
	assert.Equal(t, "MyMapPlugin", entry.GetName())
	assert.Equal(t, "zfkun", entry.GetAuthor())
	assert.Equal(t, "1.0.0", entry.GetVersion())
	assert.True(t, strings.Contains(strings.ToLower(entry.GetDescription()), "plugin"))
}