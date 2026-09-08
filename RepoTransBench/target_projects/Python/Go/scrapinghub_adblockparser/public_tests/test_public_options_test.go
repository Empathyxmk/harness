package public_tests

import (
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestPublicParseOptionsSimple(t *testing.T) {
	r := adblockparser.NewAdblockRule("/ad.js$script,domain=example.com|another.net")
	if _, ok := r.Options["script"]; !ok {
		t.Error("Expected script in options")
	}
	if dom, ok := r.Options["domain"]; !ok {
		t.Error("Expected domain in options")
	} else {
		set := dom.(map[string]struct{})
		if _, ok := set["example.com"]; !ok {
			t.Error("example.com missing from domain set")
		}
		if _, ok := set["another.net"]; !ok {
			t.Error("another.net missing from domain set")
		}
	}
}

func TestPublicParseOptionsNoOptions(t *testing.T) {
	r := adblockparser.NewAdblockRule("/track.gif")
	if len(r.Options) > 0 {
		t.Errorf("Expected empty options, got %v", r.Options)
	}
}

func TestPublicParseOptionsComplex(t *testing.T) {
	r := adblockparser.NewAdblockRule("/analytics.js$image,third-party,domain=mysite.org|anothersite.co.uk")
	if _, ok := r.Options["image"]; !ok {
		t.Error("Expected image in options")
	}
	if _, ok := r.Options["third-party"]; !ok {
		t.Error("Expected third-party in options")
	}
	if dom, ok := r.Options["domain"]; !ok {
		t.Error("Expected domain in options")
	} else {
		set := dom.(map[string]struct{})
		if _, ok := set["mysite.org"]; !ok {
			t.Error("mysite.org missing from domain set")
		}
		if _, ok := set["anothersite.co.uk"]; !ok {
			t.Error("anothersite.co.uk missing from domain set")
		}
	}
}

func TestPublicParseOptionsException(t *testing.T) {
	r := adblockparser.NewAdblockRule("@@/nocache.png$subdocument,domain=sub.example.org")
	if !r.IsException {
		t.Error("Expected exception rule")
	}
	if _, ok := r.Options["subdocument"]; !ok {
		t.Error("Expected subdocument in options")
	}
	if dom, ok := r.Options["domain"]; !ok {
		t.Error("Expected domain in options")
	} else {
		set := dom.(map[string]struct{})
		if _, ok := set["sub.example.org"]; !ok {
			t.Error("sub.example.org missing from domain set")
		}
	}
}