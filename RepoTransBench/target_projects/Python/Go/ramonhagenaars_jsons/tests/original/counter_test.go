package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpCounter(t *testing.T) {
	s := "A counter is something that counts!"
	expected := map[rune]int{
		'A': 1, ' ': 5, 'c': 2, 'o': 3, 'u': 2, 'n': 3,
		't': 5, 'e': 2, 'r': 1, 'i': 2, 's': 3, 'm': 1,
		'h': 2, 'g': 1, 'a': 1, '!': 1,
	}
	got := jsons.DumpCounter([]rune(s))
	assert.Equal(t, expected, got)
}

func TestLoadCounter(t *testing.T) {
	d := map[rune]int{
		'A': 1, ' ': 5, 'c': 2, 'o': 3, 'u': 2, 'n': 3,
		't': 5, 'e': 2, 'r': 1, 'i': 2, 's': 3, 'm': 1,
		'h': 2, 'g': 1, 'a': 1, '!': 1,
	}
	out := jsons.LoadCounter(d)
	assert.Equal(t, d, out)
}