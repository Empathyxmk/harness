package unit

import (
	"regexp"
	"strings"
	"testing"
)

var (
	ver = "1.2.3"
	ttl = "Flask-Redis"
	desc = "The ultimate Redis extension for Flask"
	url = "https://example.com/repo"
	uri = url
	author = "Author Name"
	email = "author@example.com"
	licenseVal = "MIT"
	cprt = "Copyright (C) 2023 Author"
	allList = []string{"FlaskRedis", "OtherSymbol"}
)

func TestPublicDunderConstantsDistinct(t *testing.T) {
	if _, ok := interface{}(ver).(string); !ok {
		t.Fatalf("Expected string version")
	}
	if ttl != "Flask-Redis" {
		t.Errorf("Title expected Flask-Redis, got %s", ttl)
	}
	if !strings.Contains(strings.ToLower(desc), "redis") {
		t.Fatalf("Expected 'redis' in description")
	}
	if !strings.HasPrefix(url, "https://") {
		t.Fatalf("Expected url to start with https://")
	}
	if !strings.HasPrefix(uri, "https://") {
		t.Fatalf("Expected uri to start with https://")
	}
	if !strings.Contains(email, "@") {
		t.Error("Expected @ in email")
	}
	if !strings.Contains(cprt, "opyright") {
		t.Error("Expected copyright")
	}
	if _, ok := interface{}(allList).([]string); !ok {
		t.Error("Expected []string for allList")
	}
	found := false
	for _, a := range allList {
		if a == "FlaskRedis" {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected 'FlaskRedis' in allList")
	}
}

func TestPublicTitleUnique(t *testing.T) {
	if ttl != "Flask-Redis" {
		t.Errorf("Expected Flask-Redis, got %s", ttl)
	}
	if _, ok := interface{}(author).(string); !ok {
		t.Error("Expected string author")
	}
	if len(author) <= 3 {
		t.Errorf("Expected author name > 3, got %d", len(author))
	}
}

func TestPublicVersionStyle(t *testing.T) {
	re := regexp.MustCompile(`^\d+\.\d+\.\d+`)
	if !re.MatchString(ver) {
		t.Errorf("Expected version style N.N.N, got %s", ver)
	}
}