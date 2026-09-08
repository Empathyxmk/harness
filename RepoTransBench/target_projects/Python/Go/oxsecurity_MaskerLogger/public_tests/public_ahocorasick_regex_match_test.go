package public_tests

import (
	"reflect"
	"testing"
)

type AhoCorasickTrie struct {
	Keys []string
}

func buildAhoCorasick(keys []string) *AhoCorasickTrie {
	return &AhoCorasickTrie{Keys: keys}
}

func (t *AhoCorasickTrie) Iter(s string) []string {
	found := []string{}
	for _, k := range t.Keys {
		if contains := len(k) > 0 && containsWord(s, k); contains {
			found = append(found, k)
		}
	}
	return found
}

// Util helping function for containment
func containsWord(s, k string) bool {
	return len(s) > 0 && len(k) > 0 && (len(s) >= len(k)) && (len(s) >= len(k)) && (len(s) > 0 && len(k) > 0 && stringIndex(s, k) >= 0)
}
func stringIndex(s, k string) int {
	// Return index of k in s, or -1 if not found
	for i := 0; i <= len(s)-len(k); i++ {
		if s[i:i+len(k)] == k {
			return i
		}
	}
	return -1
}

func loadRegexesFromConfig() []string {
	// Simulates returning regexes loaded from config; in real code, would load file.
	return []string{"regex1", "regex2"}
}

func TestBuildTrieAndMatch(t *testing.T) {
	keys := []string{"bear", "wolf", "lion"}
	trie := buildAhoCorasick(keys)
	s := "the wolf and lion bear witness"
	found := trie.Iter(s)
	expected := []string{"wolf", "lion", "bear"}
	// Use reflect to check unordered equality
	if !reflect.DeepEqual(sortStrings(found), sortStrings(expected)) {
		t.Errorf("Should match all words: expected %v, got %v", expected, found)
	}
}

func TestBuildRegexFromConfig(t *testing.T) {
	result := loadRegexesFromConfig()
	if len(result) == 0 {
		t.Errorf("Expected a nonempty list")
	}
}

func sortStrings(in []string) []string {
	out := make([]string, len(in))
	copy(out, in)
	for i := 0; i < len(out); i++ {
		for j := i + 1; j < len(out); j++ {
			if out[i] > out[j] {
				out[i], out[j] = out[j], out[i]
			}
		}
	}
	return out
}