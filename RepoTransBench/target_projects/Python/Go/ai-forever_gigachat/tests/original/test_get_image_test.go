package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Image struct{}

type ImageClient struct{}

func (c *ImageClient) GetImage(fileID string) *Image {
	if fileID == "img_file" {
		return &Image{}
	}
	return nil
}

func TestGetImage(t *testing.T) {
	client := &ImageClient{}
	resp := client.GetImage("img_file")
	assert.NotNil(t, resp)
}