package tests

import (
	"errors"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type CompositeImageName struct {
	name      string
	imageTags []string
}

func CreateCompositeImageName(image string, tags []string) (CompositeImageName, error) {
	name, tag, err := parseImageName(image)
	if err != nil || name == "" || strings.TrimSpace(name) == "" || name == ":" {
		return CompositeImageName{}, errors.New("MojoExecutionException")
	}
	allTags := []string{}
	if tag != "" {
		allTags = append(allTags, tag)
	}
	if tags != nil {
		allTags = append(allTags, tags...)
	} else if tag == "" {
		return CompositeImageName{}, errors.New("MojoExecutionException")
	}
	return CompositeImageName{name: name, imageTags: allTags}, nil
}

func (c CompositeImageName) GetName() string {
	return c.name
}
func (c CompositeImageName) GetImageTags() []string {
	return c.imageTags
}

func parseImageName(image string) (string, string, error) {
	if image == "" {
		return "", "", errors.New("MojoExecutionException")
	}
	// Port vs tag check (':')
	colon := strings.LastIndex(image, ":")
	slash := strings.LastIndex(image, "/")
	if colon > slash {
		return image[:colon], image[colon+1:], nil
	}
	return image, "", nil
}

func containsTag(imageName string) bool {
	colon := strings.LastIndex(imageName, ":")
	slash := strings.LastIndex(imageName, "/")
	return colon > -1 && colon > slash
}

func TestCreate_NameWithTagAndImageTags(t *testing.T) {
	cin, err := CreateCompositeImageName("repo:tag1", []string{"tag2", "tag3"})
	assert.NoError(t, err)
	assert.Equal(t, "repo", cin.GetName())
	assert.Equal(t, []string{"tag1", "tag2", "tag3"}, cin.GetImageTags())
}

func TestCreate_NameWithoutTagButWithImageTags(t *testing.T) {
	cin, err := CreateCompositeImageName("repo", []string{"tag2"})
	assert.NoError(t, err)
	assert.Equal(t, "repo", cin.GetName())
	assert.Equal(t, []string{"tag2"}, cin.GetImageTags())
}

func TestCreate_BlankName(t *testing.T) {
	_, err := CreateCompositeImageName("", []string{"atag"})
	assert.Error(t, err)
}

func TestCreate_NullTagsAndNoImageTag(t *testing.T) {
	_, err := CreateCompositeImageName("repo", nil)
	assert.Error(t, err)
}

func TestCreate_OnlyColon(t *testing.T) {
	_, err := CreateCompositeImageName(":", []string{"someTag"})
	assert.Error(t, err)
}

func TestCreate_NameWithTagNoImageTags(t *testing.T) {
	cin, err := CreateCompositeImageName("repo:foo", nil)
	assert.NoError(t, err)
	assert.Equal(t, "repo", cin.GetName())
	assert.Equal(t, []string{"foo"}, cin.GetImageTags())
}

func TestContainsTag_ColonSlashLogic(t *testing.T) {
	assert.True(t, containsTag("myregistry/origin:tag1"))
	assert.False(t, containsTag("myregistry:5000/origin"))
	assert.True(t, containsTag("image:tag"))
	assert.False(t, containsTag("image"))
}

func TestCreate_TagWithSlashAndColon(t *testing.T) {
	cin, err := CreateCompositeImageName("reg/some:image", []string{"more"})
	assert.NoError(t, err)
	assert.Equal(t, "reg/some", cin.GetName())
	assert.Equal(t, []string{"image", "more"}, cin.GetImageTags())
}