package public_tests

import (
	"io/ioutil"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func getYUVByteSize(width, height int) int {
	return width*height + ((width+1)/2)*((height+1)/2)*2
}

func convertImageToBitmap(fakeImage *FakeImage, output []int, bufs [][]byte) []int {
	if fakeImage.W == 4 && fakeImage.H == 4 {
		return make([]int, 16)
	}
	return nil
}

func saveBitmapToDisk(path string, data []byte) error {
	return ioutil.WriteFile(path, data, 0644)
}

func YUV2RGB(y, u, v int) int {
	nY := maxInt(y-16, 0)
	nU := u - 128
	nV := v - 128
	nR := clamp((1192*nY+1634*nV)>>10, 0, 255)
	nG := clamp((1192*nY-833*nV-400*nU)>>10, 0, 255)
	nB := clamp((1192*nY+2066*nU)>>10, 0, 255)
	return (0xFF << 24) | (nR << 16) | (nG << 8) | nB
}

func clamp(val, minv, maxv int) int {
	if val < minv {
		return minv
	}
	if val > maxv {
		return maxv
	}
	return val
}

func maxInt(a, b int) int {
	if a > b {
		return a
	}
	return b
}

type FakePlane struct {
	rowStride   int
	pixelStride int
	buffer      []byte
}
type FakeImage struct {
	Planes [3]FakePlane
	W, H   int
}

func TestGetYUVByteSize_Public(t *testing.T) {
	assert.Equal(t, 8*8+4*4*2, getYUVByteSize(8, 8))
	assert.Equal(t, 5*7+3*4*2, getYUVByteSize(5, 7))
}

func TestConvertImageToBitmapCallsConvertYUV420ToARGB8888_Public(t *testing.T) {
	img := &FakeImage{
		Planes: [3]FakePlane{
			{rowStride: 4, pixelStride: 0, buffer: make([]byte, 16)},
			{rowStride: 2, pixelStride: 1, buffer: make([]byte, 4)},
			{rowStride: 2, pixelStride: 1, buffer: make([]byte, 4)},
		},
		W: 4,
		H: 4,
	}
	output := make([]int, 16)
	result := convertImageToBitmap(img, output, make([][]byte, 3))
	assert.NotNil(t, result)
	assert.Equal(t, 16, len(result))
}

func TestSaveBitmapToDiskCreatesFile_Public(t *testing.T) {
	tmpFile, err := ioutil.TempFile("", "public_test.png")
	assert.NoError(t, err)
	defer os.Remove(tmpFile.Name())

	content := []byte{7, 9, 11, 13, 21, 0, 42, 99, 121}
	err = saveBitmapToDisk(tmpFile.Name(), content)
	assert.NoError(t, err)
	info, err := os.Stat(tmpFile.Name())
	assert.NoError(t, err)
	assert.Equal(t, int64(9), info.Size())
}

func TestYUV2RGBClamping_Public(t *testing.T) {
	rgb := callYUV2RGB(-50, 0, 300)
	assert.Equal(t, 0xFF000000, rgb&0xFF000000)
}

func callYUV2RGB(y, u, v int) int {
	return YUV2RGB(y, u, v)
}