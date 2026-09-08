package public_tests

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
	if err != nil || name == "" || strings.TrimSpace(name) == "" || name == ":/" {
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

func TestCreate_OtherNameWithTagAndImageTags(t *testing.T) {
	cin, err := CreateCompositeImageName("publicrepo:pub1", []string{"pub2", "pub3"})
	assert.NoError(t, err)
	assert.Equal(t, "publicrepo", cin.GetName())
	assert.Equal(t, []string{"pub1", "pub2", "pub3"}, cin.GetImageTags())
}

func TestCreate_OtherNameWithoutTagButWithDifferentImageTags(t *testing.T) {
	cin, err := CreateCompositeImageName("publicrepo", []string{"pub4"})
	assert.NoError(t, err)
	assert.Equal(t, "publicrepo", cin.GetName())
	assert.Equal(t, []string{"pub4"}, cin.GetImageTags())
}

func TestCreate_BlankDifferentName(t *testing.T) {
	_, err := CreateCompositeImageName("   ", []string{"otherTag"})
	assert.Error(t, err)
}

func TestCreate_NullTagsAndNoImageTagAgain(t *testing.T) {
	_, err := CreateCompositeImageName("anotherrepo", nil)
	assert.Error(t, err)
}

func TestCreate_InvalidColonName(t *testing.T) {
	_, err := CreateCompositeImageName(":/", []string{"pubTag"})
	assert.Error(t, err)
}

func TestCreate_NameWithTagNoImageTags_Other(t *testing.T) {
	cin, err := CreateCompositeImageName("otherrepo:bar", nil)
	assert.NoError(t, err)
	assert.Equal(t, "otherrepo", cin.GetName())
	assert.Equal(t, []string{"bar"}, cin.GetImageTags())
}

func TestContainsTag_ColonSlashDifferentLogic(t *testing.T) {
	assert.True(t, containsTag("registry2/publicorigin:mytag"))
	assert.False(t, containsTag("registry2:8080/publicorigin"))
	assert.True(t, containsTag("custom:latest"))
	assert.False(t, containsTag("custom"))
}

func TestCreate_AnotherTagWithSlashAndColon(t *testing.T) {
	cin, err := CreateCompositeImageName("myreg/pubimg:release", []string{"stable"})
	assert.NoError(t, err)
	assert.Equal(t, "myreg/pubimg", cin.GetName())
	assert.Equal(t, []string{"release", "stable"}, cin.GetImageTags())
}