package public_tests

import (
	"errors"
	"os"
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

func PushImage(_ interface{}, pushImage bool, _ string, _ interface{}, _ string, _ interface{}, _ interface{}, _ interface{}) {
	// In real impl would push; here just mock
	// Checks that call does not panic
	if pushImage {
		return
	}
}

func WriteImageInfoFile(image string, tag string, file string) error {
	// Just write JSON dummy to file
	f, err := os.Create(file)
	if err != nil {
		return err
	}
	defer f.Close()
	_, err = f.WriteString("{\"image\":\"" + image + "\", \"tag\":\"" + tag + "\"}")
	return err
}

func TestParseImageNameForAnotherFormat(t *testing.T) {
	input := "registry.example.com/newrepo/sample:mytag"
	repo, tag, err := ParseImageNameGo(input)
	assert.NoError(t, err)
	assert.Equal(t, "registry.example.com/newrepo/sample", repo)
	assert.Equal(t, "mytag", tag)
}

func TestParseImageName_WhenNoTagProvided(t *testing.T) {
	input := "ubuntu"
	repo, tag, err := ParseImageNameGo(input)
	assert.NoError(t, err)
	assert.Equal(t, "ubuntu", repo)
	assert.Equal(t, "", tag)
}

func TestPushImageNoPush(t *testing.T) {
	PushImage(nil, false, "image:tag", nil, "not/actually/used/public", nil, nil, nil)
}

func TestWriteImageInfoFile(t *testing.T) {
	file := "target/image_pub_info.json"
	_ = WriteImageInfoFile("image:pub", "imagetag", file)
	_, err := os.Stat(file)
	assert.NoError(t, err)
	_ = os.Remove(file)
}