package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMakingAnagrams_TypicalCase(t *testing.T) {
	a := "abc"
	b := "cde"
	assert.Equal(t, 4, numberNeeded(a, b))
}

func TestMakingAnagrams_IdenticalStrings(t *testing.T) {
	a := "aabbcc"
	b := "aabbcc"
	assert.Equal(t, 0, numberNeeded(a, b))
}

func TestMakingAnagrams_AllDifferent(t *testing.T) {
	a := "abc"
	b := "def"
	assert.Equal(t, 6, numberNeeded(a, b))
}

func TestMakingAnagrams_EmptyA(t *testing.T) {
	a := ""
	b := "xyz"
	assert.Equal(t, 3, numberNeeded(a, b))
}

func TestMakingAnagrams_EmptyB(t *testing.T) {
	a := "xyz"
	b := ""
	assert.Equal(t, 3, numberNeeded(a, b))
}

func TestMakingAnagrams_BothEmpty(t *testing.T) {
	assert.Equal(t, 0, numberNeeded("", ""))
}

func TestMakingAnagrams_MainTypicalCase(t *testing.T) {
	input := "abc\ncde\n"
	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainMakingAnagrams()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	output := strings.TrimSpace(string(out))
	assert.True(t, strings.HasSuffix(output, "4"))
}

// Solution stub
func numberNeeded(a, b string) int {
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

// MainMakingAnagrams simulates main.
func MainMakingAnagrams() {
	var a, b string
	fmt.Scanln(&a)
	fmt.Scanln(&b)
	fmt.Println(numberNeeded(a, b))
}