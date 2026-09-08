package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestStringsMakingAnagrams_NoOverlap(t *testing.T) {
	s1 := "abcxyz"
	s2 := "defuvw"
	assert.Equal(t, 12, numberNeededAnagrams(s1, s2))
}

func TestStringsMakingAnagrams_PartialOverlap(t *testing.T) {
	s1 := "banana"
	s2 := "bandana"
	assert.Equal(t, 2, numberNeededAnagrams(s1, s2))
}

func TestStringsMakingAnagrams_OneEmpty(t *testing.T) {
	s1 := "laptop"
	s2 := ""
	assert.Equal(t, 6, numberNeededAnagrams(s1, s2))
}

// numberNeededAnagrams as defined in original test or copied here.
func numberNeededAnagrams(a, b string) int {
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