package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestStringsMakingAnagrams_TypicalCase(t *testing.T) {
	first := "cde"
	second := "abc"
	assert.Equal(t, 4, numberNeededAnagrams(first, second))
}

func TestStringsMakingAnagrams_ReversedInputs(t *testing.T) {
	first := "abc"
	second := "cde"
	assert.Equal(t, 4, numberNeededAnagrams(first, second))
}

func TestStringsMakingAnagrams_Identical(t *testing.T) {
	first := "abcd"
	second := "abcd"
	assert.Equal(t, 0, numberNeededAnagrams(first, second))
}

func TestStringsMakingAnagrams_EmptyA(t *testing.T) {
	first := ""
	second := "aaa"
	assert.Equal(t, 3, numberNeededAnagrams(first, second))
}

func TestStringsMakingAnagrams_EmptyB(t *testing.T) {
	first := "aaa"
	second := ""
	assert.Equal(t, 3, numberNeededAnagrams(first, second))
}

func TestStringsMakingAnagrams_BothEmpty(t *testing.T) {
	assert.Equal(t, 0, numberNeededAnagrams("", ""))
}

func TestStringsMakingAnagrams_MainTypicalCase(t *testing.T) {
	input := "cde\nabc\n"
	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainStringsMakingAnagrams()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	output := strings.TrimSpace(string(out))
	assert.True(t, strings.HasSuffix(output, "4"))
}

// Solution stub
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

// MainStringsMakingAnagrams simulates main.
func MainStringsMakingAnagrams() {
	var first, second string
	fmt.Scanln(&first)
	fmt.Scanln(&second)
	fmt.Println(numberNeededAnagrams(first, second))
}