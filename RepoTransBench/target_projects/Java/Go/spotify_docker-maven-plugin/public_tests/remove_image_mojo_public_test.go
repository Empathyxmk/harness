package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type DockerClientRIMock struct {
	mock.Mock
}

func (m *DockerClientRIMock) RemoveImage(image string, force, noprune bool) error {
	args := m.Called(image, force, noprune)
	return args.Error(0)
}

func TestRemoveImageBasicPublic(t *testing.T) {
	mockCli := new(DockerClientRIMock)
	mockCli.On("RemoveImage", "imageToRemove", true, false).Return(nil).Once()
	err := mockCli.RemoveImage("imageToRemove", true, false)
	assert.NoError(t, err)
	mockCli.AssertCalled(t, "RemoveImage", "imageToRemove", true, false)
}

func TestRemoveMultipleImagesPublic(t *testing.T) {
	mockCli := new(DockerClientRIMock)
	mockCli.On("RemoveImage", mock.Anything, mock.Anything, mock.Anything).Return(nil).Maybe()
	mockCli.RemoveImage("anyone", true, false)
	mockCli.AssertCalled(t, "RemoveImage", "anyone", true, false)
}