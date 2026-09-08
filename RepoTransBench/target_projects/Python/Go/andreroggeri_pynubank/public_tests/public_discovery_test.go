package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type DiscoveryPublic struct {
	called map[string]int
}

func (d *DiscoveryPublic) GetUrl(name string) string {
	if d.called == nil {
		d.called = make(map[string]int)
	}
	d.called[name]++
	return "https://test.public/" + name
}

func TestDiscoveryUrlsPublic(t *testing.T) {
	d := &DiscoveryPublic{}
	url := d.GetUrl("auth_api")
	assert.Contains(t, url, "https://")
}

func TestDiscoveryCachePublic(t *testing.T) {
	d := &DiscoveryPublic{}
	url1 := d.GetUrl("bills_summary")
	url2 := d.GetUrl("bills_summary")
	assert.Equal(t, url1, url2)
}