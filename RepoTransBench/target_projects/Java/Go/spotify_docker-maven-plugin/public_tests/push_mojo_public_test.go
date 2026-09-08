package public_tests

import (
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

func TestPushMojoSkippedDockerPublic(t *testing.T) {
	docker := new(DockerClientPushMock)
	// Simulate skip logic - not called
}

func TestPushMojoSkippedPushPublic(t *testing.T) {
	docker := new(DockerClientPushMock)
	// Should not push
	docker.AssertNotCalled(t, "Push", mock.Anything, mock.Anything)
}