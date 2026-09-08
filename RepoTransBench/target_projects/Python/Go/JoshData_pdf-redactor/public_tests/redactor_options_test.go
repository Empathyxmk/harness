package public_tests

import (
	"reflect"
	"testing"
	pdfredactor "pdfredactor"
)

func TestPublicRedactorOptions_MetadataDefaults(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.Metadata = map[string]string{
		"Title":   "PublicTitle",
		"Subject": "PublicSubj",
		"Author":  "AuthorPerson",
	}
	if options.Metadata["Title"] != "PublicTitle" {
		t.Errorf("expected Title=PublicTitle, got %v", options.Metadata["Title"])
	}
	if options.Metadata["Subject"] != "PublicSubj" {
		t.Errorf("expected Subject=PublicSubj, got %v", options.Metadata["Subject"])
	}
	if options.Metadata["Author"] != "AuthorPerson" {
		t.Errorf("expected Author=AuthorPerson, got %v", options.Metadata["Author"])
	}
}

func TestPublicRedactorOptions_FiltersList(t *testing.T) {
	options := pdfredactor.NewRedactorOptions()
	options.ContentFilters = []pdfredactor.ContentFilter{
		{
			Pattern: "REDACT", // Simulate pattern
		},
		{
			Pattern: "SecretWord",
			Replace: func(s string) string { return "VisibleWord" },
		},
	}
	if reflect.TypeOf(options.ContentFilters).Kind() != reflect.Slice {
		t.Errorf("expected ContentFilters a slice")
	}
	if len(options.ContentFilters) != 2 {
		t.Fatalf("expected 2 content filters, got %d", len(options.ContentFilters))
	}
	if options.ContentFilters[1].Replace == nil {
		t.Errorf("expected second filter to have a replace func")
	}
}