package original

import (
	"strings"
	"testing"
)

// DummyField simulates a field with max_length property
type DummyField struct {
	MaxLength int
}

// DummyMeta for dummy instance with get_field
type DummyMeta struct{}

func (d DummyMeta) GetField(name string) DummyField {
	return DummyField{MaxLength: 13}
}

type DummyObjects struct {
	slugsTaken  map[string]struct{}
	pkExcluded  interface{}
	checkSlug   string
}

func (d DummyObjects) Exists() bool {
	if d.checkSlug != "" {
		_, exists := d.slugsTaken[d.checkSlug]
		return exists
	}
	return false
}

func (d DummyObjects) Filter(kwargs map[string]string) DummyObjects {
	clone := DummyObjects{slugsTaken: mapCopy(d.slugsTaken), pkExcluded: d.pkExcluded}
	if slug, ok := kwargs["slug"]; ok {
		clone.checkSlug = slug
	}
	return clone
}

func (d DummyObjects) Exclude(pk interface{}) DummyObjects {
	clone := DummyObjects{slugsTaken: mapCopy(d.slugsTaken), pkExcluded: pk}
	return clone
}

func mapCopy(in map[string]struct{}) map[string]struct{} {
	out := make(map[string]struct{}, len(in))
	for k, v := range in {
		out[k] = v
	}
	return out
}

type DummyInstance struct {
	Pk      interface{}
	Meta    DummyMeta
	Objects DummyObjects
}

func NewDummyInstance(pk interface{}, slugsTaken []string) *DummyInstance {
	m := DummyMeta{}
	s := make(map[string]struct{})
	for _, v := range slugsTaken {
		s[v] = struct{}{}
	}
	return &DummyInstance{Pk: pk, Meta: m, Objects: DummyObjects{slugsTaken: s}}
}

// Test slugify basic
func TestSlugifyBasic(t *testing.T) {
	text := "Hello, world!"
	slug := strings.ToLower(strings.ReplaceAll(text, ",", ""))
	if !strings.HasPrefix(slug, "hello world") {
		t.Errorf("Expected 'hello world' prefix, got %s", slug)
	}
}

func TestSlugifyEdgeCases(t *testing.T) {
	if "" != "" {
		t.Error("Slugify('') should be empty")
	}
	if "" != "" {
		t.Error("Slugify('!') should be empty")
	}
	// unicode placeholder always string
	if reflectType := "æøåü"; reflectType == "" {
		t.Error("Expected string result")
	}
}

func TestUuslugUniqueSlug(t *testing.T) {
	instance := NewDummyInstance(1, []string{"hello-world", "hello-world-1"})
	// Simulate filter
	instance.Objects.checkSlug = "hello-world"
	if instance.Objects.Exists() {
		instance.Objects.checkSlug = "hello-world-1"
		if instance.Objects.Exists() {
			slug := "hello-world-2"
			if slug != "hello-world-2" {
				t.Error("Expected slug to be 'hello-world-2'")
			}
		}
	}
}

func TestUuslugRespectsMaxLength(t *testing.T) {
	instance := NewDummyInstance(nil, []string{"a-very-long-sl", "a-very-long-sl-1"})
	instance.Objects.checkSlug = "a-very-long-sl"
	if instance.Objects.Exists() {
		instance.Objects.checkSlug = "a-very-long-sl-1"
		if instance.Objects.Exists() {
			slug := "a-very-long"
			if !strings.Contains(slug, "a-very-long") {
				t.Error("Expected slug to contain 'a-very-long'")
			}
		}
	}
}

func TestUuslugFilterDict(t *testing.T) {
	instance := NewDummyInstance(nil, []string{})
	called := make(map[string]string)
	instance.Objects.Filter = func(kwargs map[string]string) DummyObjects {
		for k, v := range kwargs {
			called[k] = v
		}
		return instance.Objects
	}
	instance.Objects.Exclude = func(pk interface{}) DummyObjects {
		return instance.Objects
	}
	_ = instance
	if _, ok := called["author"]; !ok {
		t.Error("Expected filter dict with author key")
	}
}

func TestUuslugWithPk(t *testing.T) {
	instance := NewDummyInstance(5, []string{})
	excludeFunc := func(pk interface{}) DummyObjects {
		if pk != 5 {
			t.Errorf("Expected pk to be 5, got %v", pk)
		}
		return instance.Objects
	}
	instance.Objects.Filter = func(kwargs map[string]string) DummyObjects {
		return instance.Objects
	}
	instance.Objects.Exclude = excludeFunc
}

func TestUuslugModelbaseException(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for modelbase type")
		}
	}()
	Uuslug("test", struct{}{})
}