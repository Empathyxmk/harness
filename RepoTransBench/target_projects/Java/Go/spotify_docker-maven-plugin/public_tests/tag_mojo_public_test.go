package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type DockerClientMock struct {
	mock.Mock
}

func (m *DockerClientMock) Tag(image, tag string, force bool) error {
	args := m.Called(image, tag, force)
	return args.Error(0)
}

func TestTagAlpha(t *testing.T) {
	docker := new(DockerClientMock)
	docker.On("Tag", "imageToTag", mock.AnythingOfType("string"), false).Return(nil).Once()
	mojoTag := func() {
		docker.Tag("imageToTag", "newRepo:abcdefg123", false)
	}
	mojoTag()
	docker.AssertCalled(t, "Tag", "imageToTag", mock.AnythingOfType("string"), false)
	// Simulate test of tag format
	call := docker.Calls[0]
	tag := call.Arguments[1].(string)
	parts := strings.Split(tag, ":")
	assert.Equal(t, "newRepo", parts[0])
	assert.True(t, len(parts[1]) >= 7 && strings.Index("abcdefg123", parts[1]) >= 0)
}

func TestTagBeta(t *testing.T) {
	docker := new(DockerClientMock)
	docker.On("Tag", "imageToTag", "newRepo:newTag", false).Return(nil).Once()
	func() {
		docker.Tag("imageToTag", "newRepo:newTag", false)
	}()
	docker.AssertCalled(t, "Tag", "imageToTag", "newRepo:newTag", false)
}

func TestTagSkipTagPublic(t *testing.T) {
	docker := new(DockerClientMock)
	// Should skip so not called
	docker.AssertNotCalled(t, "Tag", mock.Anything, mock.Anything, mock.Anything)
}

func TestTagSkipDockerPublic(t *testing.T) {
	// Not called at all
}