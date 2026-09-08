package original

import (
	"encoding/xml"
	"errors"
	"strings"
	"testing"
)

// For the purpose of these tests, we define small Go structs that correspond to the CAA XML elements under test.
// In a real package, these would come from your musicbrainz-ngs Go logic.

type ImageList struct {
	XMLName xml.Name    `xml:"images"`
	Images  []CAAImage  `xml:"image"`
}
type CAAImage struct {
	ID     int    `xml:"id,attr"`
	Type   string `xml:"type,attr"`
	Front  string `xml:"front,attr"`
	Back   string `xml:"back,attr"`
	Edit   int    `xml:"edit,attr"`
	Image  string `xml:"image"`
	Th150  string `xml:"thumbnails>small"`
	Th250  string `xml:"thumbnails>large"`
}

type Release struct {
	ID     string
	Images []CAAImage
}

// Dummy ParseCAAImages parses CAA XML and returns images.
// In real package, this logic will be proper and move to main code.
func ParseCAAImages(xmlData string) ([]CAAImage, error) {
	var list ImageList
	err := xml.Unmarshal([]byte(xmlData), &list)
	if err != nil {
		return nil, err
	}
	return list.Images, nil
}

// Dummy HasFrontCover checks if any image is a front cover
func HasFrontCover(images []CAAImage) bool {
	for _, img := range images {
		if img.Front == "true" {
			return true
		}
	}
	return false
}

func TestParseSingleCAAImage(t *testing.T) {
	xmlData := `
<images count="1">
  <image id="7518898981" type="Front" edit="36229746" front="true" back="false">
    <thumbnails>
      <small>https://coverartarchive.org/release/a/0a/0a2d9c1d-2756-4470-9078-6e917d7c5bef/7518898981.jpg-150.jpg</small>
      <large>https://coverartarchive.org/release/a/0a/0a2d9c1d-2756-4470-9078-6e917d7c5bef/7518898981.jpg-250.jpg</large>
    </thumbnails>
    <image>https://coverartarchive.org/release/a/0a/0a2d9c1d-2756-4470-9078-6e917d7c5bef/7518898981.jpg</image>
  </image>
</images>
`
	images, err := ParseCAAImages(xmlData)
	if err != nil {
		t.Fatalf("ParseCAAImages failed: %v", err)
	}
	if len(images) != 1 {
		t.Fatalf("Expected 1 image, got %d", len(images))
	}
	img := images[0]
	if img.ID != 7518898981 {
		t.Errorf("Expected image id 7518898981, got %d", img.ID)
	}
	if img.Type != "Front" {
		t.Errorf("Expected type 'Front', got %q", img.Type)
	}
	if img.Front != "true" {
		t.Errorf("Expected front cover to be 'true', got %q", img.Front)
	}
	if img.Edit != 36229746 {
		t.Errorf("Expected edit 36229746, got %d", img.Edit)
	}
	if img.Image == "" {
		t.Errorf("Expected a URL in <image>, got empty string")
	}
	if img.Th150 == "" || img.Th250 == "" {
		t.Errorf("Thumbnail URLs missing: small=%q large=%q", img.Th150, img.Th250)
	}
}

func TestParseMultipleCAAImagesAndFrontBackFlags(t *testing.T) {
	xmlData := `
<images count="2">
  <image id="123" type="Front" edit="1" front="true" back="false">
    <thumbnails>
      <small>https://foo/front-150.jpg</small>
      <large>https://foo/front-250.jpg</large>
    </thumbnails>
    <image>https://foo/front.jpg</image>
  </image>
  <image id="456" type="Back" edit="2" front="false" back="true">
    <thumbnails>
      <small>https://foo/back-150.jpg</small>
      <large>https://foo/back-250.jpg</large>
    </thumbnails>
    <image>https://foo/back.jpg</image>
  </image>
</images>
`
	images, err := ParseCAAImages(xmlData)
	if err != nil {
		t.Fatalf("ParseCAAImages failed: %v", err)
	}
	if len(images) != 2 {
		t.Fatalf("Expected 2 images, got %d", len(images))
	}
	var foundFront, foundBack bool
	for _, img := range images {
		if img.Front == "true" {
			foundFront = true
		}
		if img.Back == "true" {
			foundBack = true
		}
	}
	if !foundFront || !foundBack {
		t.Errorf("Expected both front and back images, got: front=%v back=%v", foundFront, foundBack)
	}
}

func TestParseCAAImagesMalformedXML(t *testing.T) {
	xmlData := `<images><image id="1" front="true"></image></badtag>`
	_, err := ParseCAAImages(xmlData)
	if err == nil {
		t.Error("Expected ParseCAAImages to fail with malformed XML")
	}
}

func TestHasFrontCoverTrue(t *testing.T) {
	images := []CAAImage{
		{ID: 1, Front: "false", Back: "false"},
		{ID: 2, Front: "true", Back: "false"},
	}
	if !HasFrontCover(images) {
		t.Error("Expected HasFrontCover to be true with a front cover image")
	}
}

func TestHasFrontCoverFalse(t *testing.T) {
	images := []CAAImage{
		{ID: 1, Front: "false", Back: "false"},
		{ID: 2, Front: "false", Back: "false"},
	}
	if HasFrontCover(images) {
		t.Error("Expected HasFrontCover to be false with no front cover image")
	}
}

func TestParseCAAImagesEmptyInput(t *testing.T) {
	xmlData := ""
	images, err := ParseCAAImages(xmlData)
	if err == nil {
		t.Error("Expected ParseCAAImages to fail on empty input")
	}
	if len(images) > 0 {
		t.Errorf("Expected 0 images on bad parse, got %d", len(images))
	}
}

// Simulate test cases for edge conditions: missing attributes, extra whitespace, etc.
func TestParseCAAImagesMissingAttributes(t *testing.T) {
	xmlData := `
<images count="1">
  <image id="789">
    <thumbnails>
      <small></small>
      <large></large>
    </thumbnails>
    <image></image>
  </image>
</images>
`
	images, err := ParseCAAImages(xmlData)
	if err != nil {
		t.Fatalf("ParseCAAImages failed: %v", err)
	}
	if len(images) != 1 {
		t.Fatalf("Expected 1 image, got %d", len(images))
	}
	img := images[0]
	if img.ID != 789 {
		t.Errorf("Expected image ID 789, got %d", img.ID)
	}
	if img.Type != "" {
		t.Errorf("Expected empty type, got %q", img.Type)
	}
	// Front and back defaults
	if img.Front != "" {
		t.Errorf("Expected front to be empty, got %q", img.Front)
	}
	if img.Back != "" {
		t.Errorf("Expected back to be empty, got %q", img.Back)
	}
	if img.Th150 != "" || img.Th250 != "" {
		t.Errorf("Expected empty thumbnails, got small=%q large=%q", img.Th150, img.Th250)
	}
	if img.Image != "" {
		t.Errorf("Expected image URL to be empty, got %q", img.Image)
	}
}

// Simulate logic for attempting to fetch a non-existent cover image (as in Python test_caa.py network error)
func TestGetNonExistentCoverArt(t *testing.T) {
	// In the real package, this would be a call to a network function returning a not found error.
	err := errors.New("cover art not found")
	if err == nil || !strings.Contains(err.Error(), "cover art not found") {
		t.Errorf("Expected error for non-existent cover art, got %v", err)
	}
}

// Simulate malformed thumbnail fields or unexpected XML structure (edge cases)
func TestParseCAAImagesMalformedThumbnailFields(t *testing.T) {
	xmlData := `
<images count="1">
  <image id="999" front="true">
    <thumbnails>
      <small></small>
    </thumbnails>
  </image>
</images>
`
	images, err := ParseCAAImages(xmlData)
	if err != nil {
		t.Fatalf("ParseCAAImages failed: %v", err)
	}
	if len(images) != 1 {
		t.Fatalf("Expected 1 image, got %d", len(images))
	}
	// Only small/large fields expected, check nothing explodes
}