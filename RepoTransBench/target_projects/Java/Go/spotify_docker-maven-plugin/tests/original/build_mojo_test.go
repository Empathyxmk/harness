package tests

// This test represents a selected subset of the logic from the verbose BuildMojoTest.java.
// It focuses on verifying that "build" and "push" Docker actions are called "when they should be", and error when not.

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type DockerClientBuildMock struct {
	mock.Mock
}

func (m *DockerClientBuildMock) Build(path, image string, handler interface{}, params ...string) error {
	args := m.Called(path, image, handler)
	return args.Error(0)
}
func (m *DockerClientBuildMock) Push(image string, handler interface{}) error {
	args := m.Called(image, handler)
	return args.Error(0)
}

type BuildMojo struct {
	Push        bool
	Image       string
	DoSkipPush  bool
	DoSkipBuild bool
}

func (b *BuildMojo) Execute(docker *DockerClientBuildMock) error {
	if b.DoSkipBuild {
		return nil
	}
	err := docker.Build("target/docker", b.Image, nil)
	if err != nil {
		return err
	}
	if !b.DoSkipPush && b.Push {
		return docker.Push(b.Image, nil)
	}
	return nil
}

func TestBuildMojoWithNoPush(t *testing.T) {
	docker := new(DockerClientBuildMock)
	docker.On("Build", "target/docker", "busybox", mock.Anything).Return(nil).Once()
	bmojo := &BuildMojo{Image: "busybox", Push: false, DoSkipPush: true}
	err := bmojo.Execute(docker)
	assert.NoError(t, err)
	docker.AssertCalled(t, "Build", "target/docker", "busybox", mock.Anything)
}

func TestBuildMojoSkipBuild(t *testing.T) {
	docker := new(DockerClientBuildMock)
	bmojo := &BuildMojo{DoSkipBuild: true}
	err := bmojo.Execute(docker)
	assert.NoError(t, err)
	docker.AssertNotCalled(t, "Build", mock.Anything, mock.Anything, mock.Anything)
}

func TestBuildWithPush(t *testing.T) {
	docker := new(DockerClientBuildMock)
	docker.On("Build", "target/docker", "busybox", mock.Anything).Return(nil).Once()
	docker.On("Push", "busybox", mock.Anything).Return(nil).Once()
	bmojo := &BuildMojo{Image: "busybox", Push: true}
	err := bmojo.Execute(docker)
	assert.NoError(t, err)
	docker.AssertCalled(t, "Push", "busybox", mock.Anything)
}

func TestBuildPushTagMissingThrows(t *testing.T) {
	docker := new(DockerClientBuildMock)
	docker.On("Build", "target/docker", "", mock.Anything).Return(errors.New("no image tag")).Once()
	bmojo := &BuildMojo{Image: ""}
	err := bmojo.Execute(docker)
	assert.Error(t, err)
}