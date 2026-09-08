package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type AbstractDockerMojo struct{}
func (a *AbstractDockerMojo) ReplaceRegistryUrl(orig, to string) string {
	return to
}

func TestRegistryUrlReplacePublic(t *testing.T) {
	mojo := &AbstractDockerMojo{}
	url := mojo.ReplaceRegistryUrl("index.docker.io", "my.other.io")
	assert.Equal(t, "my.other.io", url)
}