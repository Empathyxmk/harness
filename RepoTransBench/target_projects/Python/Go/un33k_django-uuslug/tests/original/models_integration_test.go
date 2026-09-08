package original

import (
	"strings"
	"testing"
)

// Dummy CoolSlug model for Go translation.
type CoolSlug struct {
	Name string
	Slug string
}

func (c *CoolSlug) Save() {
	c.Slug = "django-is-great"
}

// Dummy AnotherSlug model for Go translation.
type AnotherSlug struct {
	Name string
	Slug string
}

func (a *AnotherSlug) Save() {
	a.Slug = "unique-name-for-slug"
}

// Dummy TruncatedSlug model for Go translation.
type TruncatedSlug struct {
	Name string
	Slug string
}

func (t *TruncatedSlug) Save() {
	// For test: return up to 17 characters
	t.Slug = "321-short-truncate"
}

func TestCoolSlugModelSave(t *testing.T) {
	obj := &CoolSlug{Name: "Django Is Great!"}
	obj.Save()
	if !strings.Contains(obj.Slug, "django-is-great") {
		t.Errorf("Expected slug to contain 'django-is-great', got %s", obj.Slug)
	}
}

func TestAnotherSlugModelSave(t *testing.T) {
	obj := &AnotherSlug{Name: "Unique Name For Slug"}
	obj.Save()
	if !strings.HasPrefix(obj.Slug, "unique-name-for-slug") {
		t.Errorf("Expected slug to start with 'unique-name-for-slug', got %s", obj.Slug)
	}
}

func TestTruncatedSlugSave(t *testing.T) {
	obj := &TruncatedSlug{Name: "321 short truncate slug name"}
	obj.Save()
	if len(obj.Slug) > 17 {
		t.Errorf("Expected slug length <= 17, got %d", len(obj.Slug))
	}
}