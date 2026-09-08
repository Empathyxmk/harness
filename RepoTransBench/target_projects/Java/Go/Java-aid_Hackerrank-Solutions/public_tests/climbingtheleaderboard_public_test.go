package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestClimbingTheLeaderboard_CustomCase1(t *testing.T) {
	ranked := []int{120, 100, 100, 50, 40, 40, 20, 10}
	player := []int{5, 25, 45, 60, 105, 130}
	expected := []int{8, 6, 4, 4, 2, 1}
	assert.Equal(t, expected, climbingLeaderboard(ranked, player))
}

func TestClimbingTheLeaderboard_CustomCase2(t *testing.T) {
	ranked := []int{200, 180, 180, 170, 160, 160, 150, 140}
	player := []int{130, 135, 150, 175, 190, 210}
	expected := []int{9, 9, 7, 4, 2, 1}
	assert.Equal(t, expected, climbingLeaderboard(ranked, player))
}

func climbingLeaderboard(scores []int, alice []int) []int {
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
		for n > 0 && a >= unique[n-1] {
			n--
		}
		res[i] = n + 1
		n = len(unique)
	}
	return res
}