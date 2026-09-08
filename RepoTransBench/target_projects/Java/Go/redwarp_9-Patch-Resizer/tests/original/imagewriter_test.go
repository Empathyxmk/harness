package original

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

type OutputType string

const (
	PNGType OutputType = "png"
	JPGType OutputType = "jpg"
)

// Write an image to file
func ImageWriterWrite(img image.Image, format OutputType, filePath string) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()
	switch format {
	case PNGType:
		return png.Encode(file, img)
	case JPGType:
		return jpeg.Encode(file, img, &jpeg.Options{Quality: 95})
	default:
		return nil
	}
}

// Copy file contents (image aware, but does binary copy)
func ImageWriterCopy(srcPath, dstPath string) error {
	if srcPath == "" || dstPath == "" {
		return nil // do nothing, no exception as per test
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

func TestImageWriter_WritePNG(t *testing.T) {
	img := image.NewNRGBA(image.Rect(0, 0, 10, 10))
	// Draw some pixels/line
	for i := 0; i < 10; i++ {
		img.Set(i, i, color.NRGBA{255, 0, 0, 255})
	}

	tempPNG, _ := os.CreateTemp("", "testimg*.png")
	tempPNG.Close()
	defer os.Remove(tempPNG.Name())

	err := ImageWriterWrite(img, PNGType, tempPNG.Name())
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

func TestImageWriter_WriteJPG(t *testing.T) {
	img := image.NewNRGBA(image.Rect(0, 0, 10, 10))
	for i := 0; i < 10; i++ {
		img.Set(i, i, color.NRGBA{255, 0, 0, 255})
	}
	tempJPG, _ := os.CreateTemp("", "testimg*.jpg")
	tempJPG.Close()
	defer os.Remove(tempJPG.Name())

	err := ImageWriterWrite(img, JPGType, tempJPG.Name())
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

func TestImageWriter_Copy(t *testing.T) {
	img := image.NewNRGBA(image.Rect(0, 0, 10, 10))
	draw.Draw(img, img.Bounds(), image.NewUniform(color.NRGBA{255, 255, 255, 255}), image.Point{}, draw.Src)

	tempInput, _ := os.CreateTemp("", "testimginput*.png")
	err := png.Encode(tempInput, img)
	assert.NoError(t, err)
	tempInput.Close()
	defer os.Remove(tempInput.Name())

	copyFile, _ := os.CreateTemp("", "copyimg*.png")
	copyFile.Close()
	defer os.Remove(copyFile.Name())

	err = ImageWriterCopy(tempInput.Name(), copyFile.Name())
	assert.NoError(t, err)

	file, err := os.Open(copyFile.Name())
	assert.NoError(t, err)
	loaded, err := png.Decode(file)
	assert.NoError(t, err)
	assert.NotNil(t, loaded)
	file.Close()
}

func TestImageWriter_CopyNullInputs(t *testing.T) {
	err := ImageWriterCopy("", "")
	assert.NoError(t, err, "Should do nothing, no error")
}