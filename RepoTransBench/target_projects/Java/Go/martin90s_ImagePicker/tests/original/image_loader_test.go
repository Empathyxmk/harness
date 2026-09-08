package original

import (
	"testing"
)

type ImageLoader interface {
	BindImage(imageView *ImageView, uri string, width int, height int)
	BindImageSimple(imageView *ImageView, uri string)
	CreateImageView() *ImageView
	CreateFakeImageView() *ImageView
}

type ImageView struct {
	Tag interface{}
}

type DummyImageLoader struct{}

func (d *DummyImageLoader) BindImage(imageView *ImageView, uri string, width int, height int) {
	if imageView != nil && uri != "" {
		imageView.Tag = uri + string(width) + string(height)
	}
}
func (d *DummyImageLoader) BindImageSimple(imageView *ImageView, uri string) {
	if imageView != nil && uri != "" {
		imageView.Tag = uri
	}
}

func (d *DummyImageLoader) CreateImageView() *ImageView {
	return &ImageView{}
}
func (d *DummyImageLoader) CreateFakeImageView() *ImageView {
	return &ImageView{}
}

func TestImageLoader_Basic(t *testing.T) {
	loader := &DummyImageLoader{}
	image := &ImageView{}
	loader.BindImage(image, "file://x.png", 100, 200)
	if _, ok := image.Tag.(string); !ok {
		t.Error("ImageView.Tag should be string after BindImage")
	}
	loader.BindImageSimple(image, "file://x.png")
	if _, ok := image.Tag.(string); !ok {
		t.Error("ImageView.Tag should be string after BindImageSimple")
	}
	iv1 := loader.CreateImageView()
	if iv1 == nil {
		t.Error("CreateImageView should return non-nil")
	}
	iv2 := loader.CreateFakeImageView()
	if iv2 == nil {
		t.Error("CreateFakeImageView should return non-nil")
	}
}