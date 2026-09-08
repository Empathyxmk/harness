package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestDefaultReferrerPolicy(t *testing.T) {
	rp := secure.NewReferrerPolicy()
	if rp.HeaderValue() != "strict-origin-when-cross-origin" {
		t.Errorf("Expected default Referrer-Policy, got %q", rp.HeaderValue())
	}
}

func TestSetCustomPolicy(t *testing.T) {
	rp := secure.NewReferrerPolicy().Set("no-referrer")
	if rp.HeaderValue() != "no-referrer" {
		t.Errorf("Expected referrer policy 'no-referrer', got %q", rp.HeaderValue())
	}
}

func TestNoReferrer(t *testing.T) {
	rp := secure.NewReferrerPolicy().NoReferrer()
	if rp.HeaderValue() != "no-referrer" {
		t.Errorf("Expected 'no-referrer', got %q", rp.HeaderValue())
	}
}

func TestNoReferrerWhenDowngrade(t *testing.T) {
	rp := secure.NewReferrerPolicy().NoReferrerWhenDowngrade()
	if rp.HeaderValue() != "no-referrer-when-downgrade" {
		t.Errorf("Expected 'no-referrer-when-downgrade', got %q", rp.HeaderValue())
	}
}

func TestOrigin(t *testing.T) {
	rp := secure.NewReferrerPolicy().Origin()
	if rp.HeaderValue() != "origin" {
		t.Errorf("Expected 'origin', got %q", rp.HeaderValue())
	}
}

func TestOriginWhenCrossOrigin(t *testing.T) {
	rp := secure.NewReferrerPolicy().OriginWhenCrossOrigin()
	if rp.HeaderValue() != "origin-when-cross-origin" {
		t.Errorf("Expected 'origin-when-cross-origin', got %q", rp.HeaderValue())
	}
}

func TestSameOrigin(t *testing.T) {
	rp := secure.NewReferrerPolicy().SameOrigin()
	if rp.HeaderValue() != "same-origin" {
		t.Errorf("Expected 'same-origin', got %q", rp.HeaderValue())
	}
}

func TestStrictOrigin(t *testing.T) {
	rp := secure.NewReferrerPolicy().StrictOrigin()
	if rp.HeaderValue() != "strict-origin" {
		t.Errorf("Expected 'strict-origin', got %q", rp.HeaderValue())
	}
}

func TestStrictOriginWhenCrossOrigin(t *testing.T) {
	rp := secure.NewReferrerPolicy().StrictOriginWhenCrossOrigin()
	if rp.HeaderValue() != "strict-origin-when-cross-origin" {
		t.Errorf("Expected 'strict-origin-when-cross-origin', got %q", rp.HeaderValue())
	}
}

func TestUnsafeUrl(t *testing.T) {
	rp := secure.NewReferrerPolicy().UnsafeUrl()
	if rp.HeaderValue() != "unsafe-url" {
		t.Errorf("Expected 'unsafe-url', got %q", rp.HeaderValue())
	}
}

func TestClearPolicy(t *testing.T) {
	rp := secure.NewReferrerPolicy().Set("custom-policy").Clear()
	if rp.HeaderValue() != "strict-origin-when-cross-origin" {
		t.Errorf("Expected reset to default on clear, got %q", rp.HeaderValue())
	}
}