package public_tests

import (
	"image"
	"image/color"
	"image/draw"
	"image/jpeg"
	"image/png"
	"io"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Same as original test but with dimensions and public test data
type OutputType string

const (
	PNGType OutputType = "png"
	JPGType OutputType = "jpg"
)

func ImageWriterPublicWrite(img image.Image, format OutputType, filePath string) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()
	switch format {
	case PNGType:
		return png.Encode(file, img)
	case JPGType:
		return jpeg.Encode(file, img, &jpeg.Options{Quality: 98})
	default:
		return nil
	}
}

func ImageWriterPublicCopy(srcPath, dstPath string) error {
	if srcPath == "" || dstPath == "" {
		return nil // do nothing
	}
	src, err := os.Open(srcPath)
	if err != nil {
		return err
	}
	defer src.Close()
	dst, err := os.Create(dstPath)
	if err != nil {
		return err
	}
	defer dst.Close()
	_, err = io.Copy(dst, src)
	return err
}

func TestImageWriterPublic_WritePNG(t *testing.T) {
	img := image.NewNRGBA(image.Rect(0, 0, 15, 8))
	// fill rectangle and border to match Java logic
	draw.Draw(img, image.Rect(1, 1, 14, 7), image.NewUniform(color.NRGBA{0, 0, 0, 255}), image.Point{}, draw.Src)
	for x := 0; x < 15; x++ {
		img.Set(x, 0, color.NRGBA{255, 0, 0, 255})
		img.Set(x, 7, color.NRGBA{255, 0, 0, 255})
	}
	for y := 0; y < 8; y++ {
		img.Set(0, y, color.NRGBA{255, 0, 0, 255})
		img.Set(14, y, color.NRGBA{255, 0, 0, 255})
	}
	tempPNG, _ := os.CreateTemp("", "pubimg*.png")
	tempPNG.Close()
	defer os.Remove(tempPNG.Name())

	err := ImageWriterPublicWrite(img, PNGType, tempPNG.Name())
	assert.NoError(t, err)
	info, err := os.Stat(tempPNG.Name())
	assert.NoError(t, err)
	assert.False(t, info.IsDir())
	file, err := os.Open(tempPNG.Name())
	assert.NoError(t, err)
	loaded, err := png.Decode(file)
	assert.NoError(t, err)
	assert.Equal(t, img.Bounds().Dx(), loaded.Bounds().Dx())
	assert.Equal(t, img.Bounds().Dy(), loaded.Bounds().Dy())
	file.Close()
}

func TestImageWriterPublic_WriteJPG(t *testing.T) {
	img := image.NewNRGBA(image.Rect(0, 0, 15, 8))
	draw.Draw(img, image.Rect(1, 1, 14, 7), image.NewUniform(color.NRGBA{0, 0, 0, 255}), image.Point{}, draw.Src)
	for x := 0; x < 15; x++ {
		img.Set(x, 0, color.NRGBA{255, 0, 0, 255})
		img.Set(x, 7, color.NRGBA{255, 0, 0, 255})
	}
	for y := 0; y < 8; y++ {
		img.Set(0, y, color.NRGBA{255, 0, 0, 255})
		img.Set(14, y, color.NRGBA{255, 0, 0, 255})
	}
	tempJPG, _ := os.CreateTemp("", "pubimg*.jpg")
	tempJPG.Close()
	defer os.Remove(tempJPG.Name())

	err := ImageWriterPublicWrite(img, JPGType, tempJPG.Name())
	assert.NoError(t, err)
	info, err := os.Stat(tempJPG.Name())
	assert.NoError(t, err)
	assert.False(t, info.IsDir())
	file, err := os.Open(tempJPG.Name())
	assert.NoError(t, err)
	loaded, err := jpeg.Decode(file)
	assert.NoError(t, err)
	assert.Equal(t, img.Bounds().Dx(), loaded.Bounds().Dx())
	assert.Equal(t, img.Bounds().Dy(), loaded.Bounds().Dy())
	file.Close()
}

func TestImageWriterPublic_Copy(t *testing.T) {
	img := image.NewNRGBA(image.Rect(0, 0, 15, 8))
	draw.Draw(img, img.Bounds(), image.NewUniform(color.NRGBA{141, 141, 141, 255}), image.Point{}, draw.Src)

	tempInput, _ := os.CreateTemp("", "pubimginput*.png")
	err := png.Encode(tempInput, img)
	assert.NoError(t, err)
	tempInput.Close()
	defer os.Remove(tempInput.Name())

	copyFile, _ := os.CreateTemp("", "cpubimg*.png")
	copyFile.Close()
	defer os.Remove(copyFile.Name())

	err = ImageWriterPublicCopy(tempInput.Name(), copyFile.Name())
	assert.NoError(t, err)

	file, err := os.Open(copyFile.Name())
	assert.NoError(t, err)
	loaded, err := png.Decode(file)
	assert.NoError(t, err)
	assert.NotNil(t, loaded)
	file.Close()
}

func TestImageWriterPublic_CopyNullInputs(t *testing.T) {
	err := ImageWriterPublicCopy("", "")
	assert.NoError(t, err, "Should do nothing, no error")
}