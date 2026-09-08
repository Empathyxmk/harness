package tests

import (
	"errors"
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

func TestRemoveImage(t *testing.T) {
	mockCli := new(DockerClientRIMock)
	mockCli.On("RemoveImage", "imageToRemove", true, false).Return(nil).Once()
	err := mockCli.RemoveImage("imageToRemove", true, false)
	assert.NoError(t, err)
	mockCli.AssertCalled(t, "RemoveImage", "imageToRemove", true, false)
}

func TestRemoveMissingImage(t *testing.T) {
	mockCli := new(DockerClientRIMock)
	mockCli.On("RemoveImage", "imageToRemove", true, false).
		Return(errors.New("ImageNotFoundException")).Once()
	err := mockCli.RemoveImage("imageToRemove", true, false)
	assert.Error(t, err)
	mockCli.AssertCalled(t, "RemoveImage", "imageToRemove", true, false)
}

func TestRemoveImageWithTags(t *testing.T) {
	mockCli := new(DockerClientRIMock)
	mockCli.On("RemoveImage", "imageToRemove", true, false).
		Return(errors.New("ImageNotFoundException")).Once()
	mockCli.On("RemoveImage", "imageToRemove:123456", true, false).
		Return(errors.New("ImageNotFoundException")).Once()
	mockCli.On("RemoveImage", "imageToRemove:bbbbbbb", true, false).
		Return(nil).Once()
	err := mockCli.RemoveImage("imageToRemove", true, false)
	assert.Error(t, err)
	err = mockCli.RemoveImage("imageToRemove:123456", true, false)
	assert.Error(t, err)
	err = mockCli.RemoveImage("imageToRemove:bbbbbbb", true, false)
	assert.NoError(t, err)
	mockCli.AssertCalled(t, "RemoveImage", "imageToRemove:123456", true, false)
	mockCli.AssertCalled(t, "RemoveImage", "imageToRemove:bbbbbbb", true, false)
}