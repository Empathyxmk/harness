package original

import (
	"os"
	"testing"
	"lancegin_haishoku/haishoku/haillow"
)

func TestGetImageLocal(t *testing.T) {
	img, err := haillow.GetImage("test/sample.png")
	if err != nil {
		t.Fatalf("GetImage: %v", err)
	}
	if img.Mode() != "RGB" {
		t.Errorf("GetImage mode = %s; want RGB", img.Mode())
	}
}

func TestGetImageConvert(t *testing.T) {
	img, err := haillow.GetImage("test/sample_gray.png")
	if err != nil {
		t.Fatalf("GetImage (gray): %v", err)
	}
	if img.Mode() != "RGB" {
		t.Errorf("GetImage gray mode = %s; want RGB", img.Mode())
	}
}

func TestGetThumbnail(t *testing.T) {
	img, _ := haillow.GetImage("test/sample.png")
	thumb := haillow.GetThumbnail(img)
	if thumb.Width() > 256 || thumb.Height() > 256 {
		t.Errorf("Thumbnail size > 256")
	}
}

func TestGetColors(t *testing.T) {
	colors, err := haillow.GetColors("test/sample.png")
	if err != nil {
		t.Fatalf("GetColors: %v", err)
	}
	if len(colors) == 0 {
		t.Error("GetColors returned no colors")
	}
}

func TestNewImage(t *testing.T) {
	img := haillow.NewImage("RGB", 8, 9, [3]int{1, 2, 3})
	if img.Width() != 8 || img.Height() != 9 {
		t.Errorf("NewImage size = (%d,%d); want (8,9)", img.Width(), img.Height())
	}
}

func TestJointImage(t *testing.T) {
	imgs := []haillow.Image{
		haillow.NewImage("RGB", 50, 20, [3]int{0, 0, 0}),
		haillow.NewImage("RGB", 50, 20, [3]int{20, 0, 30}),
		haillow.NewImage("RGB", 50, 20, [3]int{40, 0, 60}),
		haillow.NewImage("RGB", 50, 20, [3]int{60, 0, 90}),
	}
	if err := haillow.JointImage(imgs); err != nil {
		t.Fatalf("JointImage failed: %v", err)
	}
}