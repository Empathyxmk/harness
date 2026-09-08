package tests

import (
	"errors"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func ParseImageNameGo(imageName string) (string, string, error) {
	if imageName == "" {
		return "", "", errors.New("MojoExecutionException")
	}
	colon := strings.LastIndex(imageName, ":")
	slash := strings.LastIndex(imageName, "/")
	if colon > slash {
		base := imageName[:colon]
		tag := imageName[colon+1:]
		if tag == "" {
			return base, "", nil
		}
		return base, tag, nil
	}
	return imageName, "", nil
}

func TestParseImageName_Tagged(t *testing.T) {
	repo, tag, err := ParseImageNameGo("foo/bar:latest")
	assert.NoError(t, err)
	assert.Equal(t, "foo/bar", repo)
	assert.Equal(t, "latest", tag)
}

func TestParseImageName_NoTag(t *testing.T) {
	repo, tag, err := ParseImageNameGo("foo/bar")
	assert.NoError(t, err)
	assert.Equal(t, "foo/bar", repo)
	assert.Equal(t, "", tag)
}

func TestParseImageName_RepoPort(t *testing.T) {
	repo, tag, err := ParseImageNameGo("myregistry:4000/bar")
	assert.NoError(t, err)
	assert.Equal(t, "myregistry:4000/bar", repo)
	assert.Equal(t, "", tag)
}

func TestParseImageName_EmptyTag(t *testing.T) {
	repo, tag, err := ParseImageNameGo("foo/bar:")
	assert.NoError(t, err)
	assert.Equal(t, "foo/bar", repo)
	assert.Equal(t, "", tag)
}

func TestParseImageName_Error(t *testing.T) {
	_, _, err := ParseImageNameGo("")
	assert.Error(t, err)
}