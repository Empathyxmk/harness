package original

import (
	"testing"
	"github.com/yourusername/wikipediaapi"
)

func TestMissingUserAgentShouldFail(t *testing.T) {
	defer testutil.ExpectPanicContains(t, "user agent")()
	wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "en",
	})
}

func TestSwappedParametersInConstructor(t *testing.T) {
	defer testutil.ExpectPanicContains(t, "user agent")()
	wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "en",
		Language: "my-user-agent",
	})
}

func TestEmptyParametersInConstructor(t *testing.T) {
	defer testutil.ExpectPanicContains(t, "user agent")()
	wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "",
		Language: "",
	})
}

func TestEmptyLanguageInConstructor(t *testing.T) {
	defer testutil.ExpectPanicContains(t, "language")()
	wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "test-user-agent",
		Language: "",
	})
}

func TestLongLanguageAndUserAgent(t *testing.T) {
	wiki := wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "param-user-agent",
		Language:  "very-long-language",
	})
	if wiki == nil {
		t.Fatal("wiki is nil")
	}
	if wiki.Language != "very-long-language" {
		t.Errorf("Expected language 'very-long-language', got '%v'", wiki.Language)
	}
	if wiki.Variant != "" {
		t.Errorf("Expected Variant to be empty, got '%v'", wiki.Variant)
	}
}

func TestUserAgentIsUsed(t *testing.T) {
	wiki := wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "param-user-agent",
	})
	if wiki == nil {
		t.Fatal("wiki is nil")
	}
	userAgent := wiki.UserAgentString()
	if userAgent != "param-user-agent ("+wikipediaapi.USER_AGENT+")" {
		t.Errorf("Expected user-agent: param-user-agent (%v), got %v", wikipediaapi.USER_AGENT, userAgent)
	}
	if wiki.Language != "en" {
		t.Errorf("Expected default language en, got %v", wiki.Language)
	}
}

func TestUserAgentInHeadersIsFine(t *testing.T) {
	wiki := wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "en",
		Headers:   map[string]string{"User-Agent": "header-user-agent"},
	})
	if wiki == nil {
		t.Fatal("wiki is nil")
	}
	userAgent := wiki.UserAgentString()
	if userAgent != "header-user-agent ("+wikipediaapi.USER_AGENT+")" {
		t.Errorf("Expected User-Agent override, got %v", userAgent)
	}
}

func TestUserAgentInHeadersWin(t *testing.T) {
	wiki := wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
		UserAgent: "param-user-agent",
		Headers:   map[string]string{"User-Agent": "header-user-agent"},
	})
	if wiki == nil {
		t.Fatal("wiki is nil")
	}
	userAgent := wiki.UserAgentString()
	if userAgent != "header-user-agent ("+wikipediaapi.USER_AGENT+")" {
		t.Errorf("Expected User-Agent override, got %v", userAgent)
	}
}