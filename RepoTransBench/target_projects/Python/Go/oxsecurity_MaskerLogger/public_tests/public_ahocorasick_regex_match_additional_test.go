package public_tests

import (
	"testing"
)

func TestEmptyTrie(t *testing.T) {
	trie := buildAhoCorasick([]string{})
	matches := trie.Iter("this string has nothing of interest")
	if len(matches) != 0 {
		t.Errorf("Expected no matches in empty trie, got: %v", matches)
	}
}

func TestPartialMatchNotFound(t *testing.T) {
	trie := buildAhoCorasick([]string{"dog", "cat", "mouse"})
	s := "The quick brown fox."
	found := trie.Iter(s)
	if len(found) != 0 {
		t.Errorf("Expected no matches for absent keys, got: %v", found)
	}
}