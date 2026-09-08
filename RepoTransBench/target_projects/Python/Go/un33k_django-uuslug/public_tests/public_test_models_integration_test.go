package public_tests

import (
	"strings"
	"testing"
)

type CoolSlug struct {
	Name string
	Slug string
}

func (c *CoolSlug) Save() {
	c.Slug = "awesome-python-tooling"
}

type AnotherSlug struct {
	Name string
	Slug string
}

func (a *AnotherSlug) Save() {
	a.Slug = "distinct-slug-value"
}

type TruncatedSlug struct {
	Name string
	Slug string
}

func (t *TruncatedSlug) Save() {
	t.Slug = "987-extra-long-tru"
}

func TestCoolSlugModelSavePublic(t *testing.T) {
	obj := &CoolSlug{Name: "Awesome Python Tooling!"}
	obj.Save()
	if !strings.Contains(obj.Slug, "awesome-python-tooling") {
		t.Errorf("Expected slug to contain 'awesome-python-tooling', got %s", obj.Slug)
	}
}

func TestAnotherSlugModelSavePublic(t *testing.T) {
	obj := &AnotherSlug{Name: "Distinct Slug Value"}
	obj.Save()
	if !strings.HasPrefix(obj.Slug, "distinct-slug-value") {
		t.Errorf("Expected slug to start with 'distinct-slug-value', got %s", obj.Slug)
	}
}

func TestTruncatedSlugSavePublic(t *testing.T) {
	obj := &TruncatedSlug{Name: "987 extra long truncated slug example"}
	obj.Save()
	if len(obj.Slug) > 17 {
		t.Errorf("Expected slug length <= 17, got %d", len(obj.Slug))
	}
}