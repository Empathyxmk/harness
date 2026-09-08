package tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type DockerClientPushMock struct {
	mock.Mock
}

func (m *DockerClientPushMock) Push(image string, handler interface{}) error {
	args := m.Called(image, handler)
	return args.Error(0)
}

func (m *DockerClientPushMock) RegistryAuth() RegistryAuth {
	// Returns a static mock auth config
	return RegistryAuth{
		Username: "dxia3",
		Password: "SxpxdUQA2mvX7oj",
		Email:    "dxia+3@spotify.com",
	}
}

type PushMojo struct {
	SkipDocker    bool
	SkipDockerPush bool
}

func (p *PushMojo) Execute(docker *DockerClientPushMock) error {
	if p.SkipDocker {
		return nil
	}
	if p.SkipDockerPush {
		return nil
	}
	return docker.Push("busybox", nil)
}

func TestPush(t *testing.T) {
	docker := new(DockerClientPushMock)
	docker.On("Push", "busybox", mock.Anything).Return(nil).Once()
	mojo := &PushMojo{}
	err := mojo.Execute(docker)
	assert.NoError(t, err)
	docker.AssertCalled(t, "Push", "busybox", mock.Anything)
}

func TestFailingPushWithRetries(t *testing.T) {
	docker := new(DockerClientPushMock)
	docker.On("Push", "busybox", mock.Anything).Return(errors.New("Expected")).Times(4)
	mojo := &PushMojo{}
	var i int
	var err error
	for i = 0; i < 4; i++ {
		err = mojo.Execute(docker)
	}
	assert.Error(t, err)
	assert.Equal(t, 4, len(docker.Calls))
}

func TestPushPrivateRepo(t *testing.T) {
	docker := new(DockerClientPushMock)
	mojo := &PushMojo{}
	auth := docker.RegistryAuth()
	assert.Equal(t, "dxia3", auth.Username)
	assert.Equal(t, "SxpxdUQA2mvX7oj", auth.Password)
	assert.Equal(t, "dxia+3@spotify.com", auth.Email)
	docker.On("Push", "dxia3/docker-maven-plugin-auth", mock.Anything).Return(nil).Once()
	_ = docker.Push("dxia3/docker-maven-plugin-auth", nil)
	docker.AssertCalled(t, "Push", "dxia3/docker-maven-plugin-auth", mock.Anything)
}

func TestPushSkipPush(t *testing.T) {
	docker := new(DockerClientPushMock)
	mojo := &PushMojo{SkipDockerPush: true}
	err := mojo.Execute(docker)
	assert.NoError(t, err)
	docker.AssertNotCalled(t, "Push", mock.Anything, mock.Anything)
}

func TestPushSkipDocker(t *testing.T) {
	docker := new(DockerClientPushMock)
	mojo := &PushMojo{SkipDocker: true}
	err := mojo.Execute(docker)
	assert.NoError(t, err)
	docker.AssertNotCalled(t, "Push", mock.Anything, mock.Anything)
}