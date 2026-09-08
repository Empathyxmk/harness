package original

import (
    "testing"
    "github.com/yourusername/wikipediaapi"
)

func TestWikipediaInitMinimal(t *testing.T) {
    wiki := wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
        UserAgent: "test/1.0",
        Language: "en",
    })
    if wiki == nil {
        t.Fatal("Expected non-nil wiki instance")
    }
    if wiki.Language != "en" {
        t.Errorf("Expected language en, got %v", wiki.Language)
    }
    if wiki.ExtractFormat != wikipediaapi.ExtractFormatWIKI {
        t.Errorf("Expected ExtractFormatWIKI, got %v", wiki.ExtractFormat)
    }
}

func TestWikipediaInitAllArgs(t *testing.T) {
    wiki := wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
        UserAgent: "test/2.0",
        Language:  "de",
        Variant:   "bar",
        ExtractFormat: wikipediaapi.ExtractFormatHTML,
        Headers:      map[string]string{"Foo": "Bar"},
        ExtraAPIParams: map[string]string{"baz": "qux"},
        Timeout: 1,
    })
    if wiki.Language != "de" {
        t.Errorf("Expected language de, got %v", wiki.Language)
    }
    if wiki.Variant != "bar" {
        t.Errorf("Expected variant bar, got %v", wiki.Variant)
    }
    if wiki.ExtractFormat != wikipediaapi.ExtractFormatHTML {
        t.Errorf("Expected ExtractFormatHTML, got %v", wiki.ExtractFormat)
    }
}

func TestWikipediaInitShortUserAgentRaises(t *testing.T) {
    defer func() {
        if r := recover(); r == nil {
            t.Error("Expected panic for short user agent but did not panic")
        }
    }()
    _ = wikipediaapi.NewWikipedia(&wikipediaapi.WikipediaConfig{
        UserAgent: "bot",
        Language: "en",
    })
}