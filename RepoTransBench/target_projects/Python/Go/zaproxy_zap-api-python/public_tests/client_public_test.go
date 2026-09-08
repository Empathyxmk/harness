package public_tests

import (
	"testing"
	"strings"
	"github.com/stretchr/testify/assert"
)

type CoreModule struct{}

func (c *CoreModule) Title() string  { return "OWASP ZAP API" }
func (c *CoreModule) Banner() string { return "[OWASP ZAP] Proxy Banner" }

func TestClientTitleNewCase(t *testing.T) {
	core := &CoreModule{}
	title := core.Title()
	assert.IsType(t, "", title)
	assert.True(t, len(title) > 3)
}

func TestClientBannerNewCase(t *testing.T) {
	core := &CoreModule{}
	banner := core.Banner()
	assert.True(t, strings.Contains(banner, "ZAP") || strings.Contains(banner, "Proxy"))
}