package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestClimbingTheLeaderboard_TypicalCase(t *testing.T) {
	scores := []int{100, 100, 50, 40, 40, 20, 10}
	alice := []int{5, 25, 50, 120}
	expected := []int{6, 4, 2, 1}
	assert.Equal(t, expected, climbingLeaderboard(scores, alice))
}

func TestClimbingTheLeaderboard_AllScoresSame(t *testing.T) {
	scores := []int{100, 100, 100}
	alice := []int{50, 100, 101}
	expected := []int{2, 1, 1}
	assert.Equal(t, expected, climbingLeaderboard(scores, alice))
}

func TestClimbingTheLeaderboard_AliceAllLower(t *testing.T) {
	scores := []int{60, 30, 10}
	alice := []int{5, 3}
	expected := []int{4, 4}
	assert.Equal(t, expected, climbingLeaderboard(scores, alice))
}

func TestClimbingTheLeaderboard_AliceAllHigher(t *testing.T) {
	scores := []int{40, 20, 10}
	alice := []int{50}
	expected := []int{1}
	assert.Equal(t, expected, climbingLeaderboard(scores, alice))
}

func TestClimbingTheLeaderboard_SingleElementScores(t *testing.T) {
	scores := []int{100}
	alice := []int{100, 101, 99}
	expected := []int{1, 1, 2}
	assert.Equal(t, expected, climbingLeaderboard(scores, alice))
}

func TestClimbingTheLeaderboard_BinarySearch(t *testing.T) {
	a := []int{100, 90, 80, 70, 70, 60}
	assert.Equal(t, 3, binarySearch(a, 70))
	assert.Equal(t, 2, binarySearch(a, 85))
	assert.Equal(t, 1, binarySearch(a, 95))
	assert.Equal(t, -1, binarySearch(a, 50))
}

func TestClimbingTheLeaderboard_MainTypicalCase(t *testing.T) {
	input := "7\n100 100 50 40 40 20 10\n4\n5 25 50 120\n"
	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainClimbingTheLeaderboard()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	outStr := string(out)
	assert.True(t, strings.Contains(outStr, "1") && strings.Contains(outStr, "6"))
}

// Solution stubs for ClimbingTheLeaderboard
func climbingLeaderboard(scores []int, alice []int) []int {
	// Remove duplicate ranks and preserve descending order
	unique := make([]int, 0, len(scores))
	m := make(map[int]struct{})
	for _, s := range scores {
		if _, ok := m[s]; !ok {
			unique = append(unique, s)
			m[s] = struct{}{}
		}
	}
	n := len(unique)
	res := make([]int, len(alice))
	for i, a := range alice {
		// linear search from end
		for n > 0 && a >= unique[n-1] {
			n--
		}
		res[i] = n + 1
		n = len(unique)
	}
	return res
}

// binarySearch returns the index of first score not greater than target, for testing.
func binarySearch(a []int, target int) int {
	for i, v := range a {
		if v <= target {
			return i
		}
	}
	return -1
}

// MainClimbingTheLeaderboard simulates main().
func MainClimbingTheLeaderboard() {
	var n int
	fmt.Scanf("%d\n", &n)
	line := ""
	fmt.Scanln(&line)
	fields := strings.Fields(line)
	scores := make([]int, n)
	for i, s := range fields {
		fmt.Sscanf(s, "%d", &scores[i])
	}
	var m int
	fmt.Scanf("%d\n", &m)
	line2 := ""
	fmt.Scanln(&line2)
	fields2 := strings.Fields(line2)
	alice := make([]int, m)
	for i, s := range fields2 {
		fmt.Sscanf(s, "%d", &alice[i])
	}
	ranks := climbingLeaderboard(scores, alice)
	for _, r := range ranks {
		fmt.Println(r)
	}
}