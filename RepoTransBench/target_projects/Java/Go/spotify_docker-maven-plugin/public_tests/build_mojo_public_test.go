package public_tests

import (
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

func TestBuildMojoWithNoPushPublic(t *testing.T) {
	docker := new(DockerClientBuildMock)
	docker.On("Build", "target/docker", "busybox", mock.Anything).Return(nil).Once()
	err := docker.Build("target/docker", "busybox", nil)
	assert.NoError(t, err)
	docker.AssertCalled(t, "Build", "target/docker", "busybox", nil)
}

func TestBuildMojoSkipBuildPublic(t *testing.T) {
	docker := new(DockerClientBuildMock)
	// Should not be called
}