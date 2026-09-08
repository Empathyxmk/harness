package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type Discovery struct{}

func (d *Discovery) GetUrl(name string) (string, error) {
	if name == "some-url" {
		return "", errors.New("not found")
	}
	return "https://example.com/token", nil
}

func (d *Discovery) GetAppUrl(name string) (string, error) {
	if name == "lift" {
		return "https://example.com/lift", nil
	}
	return "", errors.New("not found")
}

func TestGetUnexistentUrl(t *testing.T) {
	d := &Discovery{}
	_, err := d.GetUrl("some-url")
	assert.Error(t, err)
}

func TestGetUrl(t *testing.T) {
	d := &Discovery{}
	url, err := d.GetUrl("token")
	assert.NoError(t, err)
	assert.Contains(t, url, "https://")
}

func TestGetAppUrl(t *testing.T) {
	d := &Discovery{}
	url, err := d.GetAppUrl("lift")
	assert.NoError(t, err)
	assert.Contains(t, url, "https://")
}