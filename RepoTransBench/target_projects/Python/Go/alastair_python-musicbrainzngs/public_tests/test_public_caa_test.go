package public_tests

import (
	"fmt"
	"testing"
)

func makeReleaseURL(mbid string) string {
	return fmt.Sprintf("http://coverartarchive.org/release/%s", mbid)
}

func makeReleaseGroupURL(mbid string) string {
	return fmt.Sprintf("http://coverartarchive.org/release-group/%s", mbid)
}

// Like python test: params are optional
func makeImageURL(mbid string, num int, width *int, imageType *string) string {
	url := fmt.Sprintf("http://coverartarchive.org/release/%s/%d", mbid, num)
	params := ""
	if width != nil || imageType != nil {
		params = "?"
		if width != nil {
			params += fmt.Sprintf("width=%d", *width)
			if imageType != nil {
				params += "&"
			}
		}
		if imageType != nil {
			params += fmt.Sprintf("type=%s", *imageType)
		}
	}
	return url + params
}

func TestPublicMakeReleaseURL(t *testing.T) {
	mbid := "12345678-abcd-1234-ef00-123456abcdef"
	expected := "http://coverartarchive.org/release/12345678-abcd-1234-ef00-123456abcdef"
	got := makeReleaseURL(mbid)
	if got != expected {
		t.Fatalf("expected %s, got %s", expected, got)
	}
}

func TestPublicMakeReleaseGroupURL(t *testing.T) {
	mbid := "76fedcba-dcba-4321-ba09-fedcba765432"
	expected := "http://coverartarchive.org/release-group/76fedcba-dcba-4321-ba09-fedcba765432"
	got := makeReleaseGroupURL(mbid)
	if got != expected {
		t.Fatalf("expected %s, got %s", expected, got)
	}
}

func TestPublicMakeCoverartURLWithParams(t *testing.T) {
	mbid := "abcdef01-2345-6789-bcdf-abcdef098765"
	width := 600
	imgType := "front"
	got := makeImageURL(mbid, 1, &width, &imgType)
	expected := "http://coverartarchive.org/release/abcdef01-2345-6789-bcdf-abcdef098765/1?width=600&type=front"
	if got != expected {
		t.Fatalf("expected %s, got %s", expected, got)
	}
}