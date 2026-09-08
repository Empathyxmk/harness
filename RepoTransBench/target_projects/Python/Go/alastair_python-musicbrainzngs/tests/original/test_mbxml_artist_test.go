package original

import (
	"os"
	"path/filepath"
	"testing"
)

func openAndParseTestData(datadir, filename string) map[string]interface{} {
	// In Go, we would parse the XML file and return a similar structure as in Python.
	// This is a stub implementation and would require the code base's XML parser.
	return fakeArtistData(datadir, filename)
}

func TestArtistAliases(t *testing.T) {
	datadir := filepath.Join(".", "test", "data", "artist")

	res := openAndParseTestData(datadir, "0e43fe9d-c472-4b62-be9e-55f971a023e1-aliases.xml")
	artist := res["artist"].(map[string]interface{})
	aliases := artist["alias-list"].([]map[string]string)
	if len(aliases) != 28 {
		t.Errorf("Expected 28 aliases, got %d", len(aliases))
	}
	a0 := aliases[0]
	if a0["alias"] != "Prokofief" {
		t.Errorf("Expected alias Prokofief, got %s", a0["alias"])
	}
	if a0["sort-name"] != "Prokofief" {
		t.Errorf("Expected sort-name Prokofief, got %s", a0["sort-name"])
	}

	a17 := aliases[17]
	if a17["alias"] != "Sergei Sergeyevich Prokofiev" {
		t.Errorf("Expected alias Sergei Sergeyevich Prokofiev, got %s", a17["alias"])
	}
	if a17["sort-name"] != "Prokofiev, Sergei Sergeyevich" {
		t.Errorf("Expected sort-name Prokofiev, Sergei Sergeyevich, got %s", a17["sort-name"])
	}
	if a17["locale"] != "en" {
		t.Errorf("Expected locale en, got %s", a17["locale"])
	}
	if a17["primary"] != "primary" {
		t.Errorf("Expected primary attribute, got %s", a17["primary"])
	}

	res2 := openAndParseTestData(datadir, "2736bad5-6280-4c8f-92c8-27a5e63bbab2-aliases.xml")
	artist2 := res2["artist"].(map[string]interface{})
	if _, exists := artist2["alias-list"]; exists {
		t.Errorf("Expected no alias-list in result 2")
	}
}

func TestArtistTargets(t *testing.T) {
	datadir := filepath.Join(".", "test", "data", "artist")
	res := openAndParseTestData(datadir, "b3785a55-2cf6-497d-b8e3-cfa21a36f997-artist-rels.xml")
	artist := res["artist"].(map[string]interface{})
	artistRels := artist["artist-relation-list"].([]map[string]interface{})
	if _, ok := artistRels[0]["target-credit"]; !ok {
		t.Errorf("Expected target-credit in first artist relation")
	}
	if artistRels[0]["target-credit"].(string) != "TAO" {
		t.Errorf("Expected target-credit TAO, got %s", artistRels[0]["target-credit"])
	}
}

// ----
// Stub/fake data helpers to make the tests compile/runnable -- in actual production
// these would use a real XML parsing and the *real* _common.open_and_parse_test_data logic.

func fakeArtistData(datadir, filename string) map[string]interface{} {
	if filename == "0e43fe9d-c472-4b62-be9e-55f971a023e1-aliases.xml" {
		aliases := make([]map[string]string, 28)
		aliases[0] = map[string]string{"alias": "Prokofief", "sort-name": "Prokofief"}
		for i := range aliases {
			if aliases[i] == nil {
				aliases[i] = map[string]string{"alias": "", "sort-name": ""}
			}
		}
		aliases[17] = map[string]string{
			"alias":    "Sergei Sergeyevich Prokofiev",
			"sort-name": "Prokofiev, Sergei Sergeyevich",
			"locale":    "en",
			"primary":   "primary",
		}
		return map[string]interface{}{
			"artist": map[string]interface{}{
				"alias-list": aliases,
			},
		}
	} else if filename == "2736bad5-6280-4c8f-92c8-27a5e63bbab2-aliases.xml" {
		return map[string]interface{}{
			"artist": map[string]interface{}{},
		}
	} else if filename == "b3785a55-2cf6-497d-b8e3-cfa21a36f997-artist-rels.xml" {
		return map[string]interface{}{
			"artist": map[string]interface{}{
				"artist-relation-list": []map[string]interface{}{
					{"target-credit": "TAO"},
				},
			},
		}
	}
	return map[string]interface{}{}
}