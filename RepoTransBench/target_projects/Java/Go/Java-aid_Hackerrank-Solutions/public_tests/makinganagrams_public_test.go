package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMakingAnagrams_DifferentLetters(t *testing.T) {
	s1 := "game"
	s2 := "team"
	assert.Equal(t, 3, makeAnagram(s1, s2))
}

func TestMakingAnagrams_OneStringEmpty(t *testing.T) {
	s1 := "football"
	s2 := ""
	assert.Equal(t, 8, makeAnagram(s1, s2))
}

func TestMakingAnagrams_BothStringsTheSame(t *testing.T) {
	s1 := "network"
	s2 := "network"
	assert.Equal(t, 0, makeAnagram(s1, s2))
}

// makeAnagram as defined in MakingAnagrams
func makeAnagram(a, b string) int {
	count := make([]int, 26)
	for _, ch := range a {
		count[ch-'a']++
	}
	for _, ch := range b {
		count[ch-'a']--
	}
	sum := 0
	for _, v := range count {
		if v < 0 {
			v = -v
		}
		sum += v
	}
	return sum
}