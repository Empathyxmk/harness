package tests

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
func (m *DockerClientMock) Push(tag string, handler interface{}) error {
	args := m.Called(tag, handler)
	return args.Error(0)
}

type TagMojo struct {
	SkipDocker    bool
	SkipDockerTag bool
}

func (t *TagMojo) Execute(docker *DockerClientMock) {
	if t.SkipDocker {
		return
	}
	if t.SkipDockerTag {
		return
	}
	docker.Tag("imageToTag", "newRepo:newTag", false)
	docker.Push("newRepo:newTag", nil)
}

func TestTag1(t *testing.T) {
	docker := new(DockerClientMock)
	docker.On("Tag", "imageToTag", "newRepo:newTag", false).Return(nil).Once()
	docker.On("Push", "newRepo:newTag", mock.Anything).Return(nil).Once()
	mojo := &TagMojo{}
	mojo.Execute(docker)
	docker.AssertCalled(t, "Tag", "imageToTag", "newRepo:newTag", false)
	docker.AssertCalled(t, "Push", "newRepo:newTag", mock.Anything)
}

func TestTag2(t *testing.T) {
	docker := new(DockerClientMock)
	docker.On("Tag", "imageToTag", mock.AnythingOfType("string"), false).Return(nil).Once()
	mojo := &TagMojo{}
	mojo.Execute(docker)
	docker.AssertCalled(t, "Tag", "imageToTag", mock.AnythingOfType("string"), false)
	// Test the tag format
	call := docker.Calls[0]
	tag := call.Arguments[1].(string)
	parts := strings.Split(tag, ":")
	assert.Equal(t, "newRepo", parts[0])
	assert.True(t, len(parts[1]) >= 7)
}

func TestTag3(t *testing.T) {
	docker := new(DockerClientMock)
	docker.On("Tag", "imageToTag", "newRepo:newTag", false).Return(nil).Once()
	mojo := &TagMojo{}
	mojo.Execute(docker)
	docker.AssertCalled(t, "Tag", "imageToTag", "newRepo:newTag", false)
}

func TestTagSkipTag(t *testing.T) {
	docker := new(DockerClientMock)
	mojo := &TagMojo{SkipDockerTag: true}
	mojo.Execute(docker)
	docker.AssertNotCalled(t, "Tag", mock.Anything, mock.Anything, mock.Anything)
}

func TestTagSkipDocker(t *testing.T) {
	docker := new(DockerClientMock)
	mojo := &TagMojo{SkipDocker: true}
	mojo.Execute(docker)
	docker.AssertNotCalled(t, "Tag", mock.Anything, mock.Anything, mock.Anything)
}