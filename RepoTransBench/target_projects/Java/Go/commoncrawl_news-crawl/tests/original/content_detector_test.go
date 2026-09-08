package tests

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ContentDetector struct {
	clues     [][]string
	maxOffset int
}

func NewContentDetector(clues [][]string, maxOffset int) *ContentDetector {
	return &ContentDetector{clues: clues, maxOffset: maxOffset}
}

func (d *ContentDetector) getFirstMatch(content []byte) int {
	searchLen := len(content)
	if searchLen > d.maxOffset {
		searchLen = d.maxOffset
	}
	searchContent := content[:searchLen]
	for i, clueGroup := range d.clues {
		match := true
		for _, subclue := range clueGroup {
			if !bytes.Contains(searchContent, []byte(subclue)) {
				match = false
				break
			}
		}
		if match {
			return i
		}
	}
	return -1
}

func (d *ContentDetector) matches(content []byte) bool {
	return d.getFirstMatch(content) != -1
}

func TestSimpleOrMatch(t *testing.T) {
	clues := [][]string{{"foo"}, {"bar"}}
	detector := NewContentDetector(clues, 100)
	assert.Equal(t, 0, detector.getFirstMatch([]byte("foo hello world")))
	assert.Equal(t, 1, detector.getFirstMatch([]byte("something bar here")))
	assert.Equal(t, -1, detector.getFirstMatch([]byte("baz qux")))
}

func TestAndMatch(t *testing.T) {
	clues := [][]string{{"foo", "bar"}, {"baz"}}
	detector := NewContentDetector(clues, 100)
	assert.Equal(t, 0, detector.getFirstMatch([]byte("this line has foo and bar together")))
	assert.Equal(t, 1, detector.getFirstMatch([]byte("some baz string")))
	assert.Equal(t, -1, detector.getFirstMatch([]byte("foo only here")))
}

func TestMaxOffset(t *testing.T) {
	clues := [][]string{{"clue"}}
	detector := NewContentDetector(clues, 4)
	assert.Equal(t, -1, detector.getFirstMatch([]byte("say clue later")))
	assert.Equal(t, 0, detector.getFirstMatch([]byte("clue here")))
}

func TestMatchesConvenience(t *testing.T) {
	clues := [][]string{{"needle"}}
	detector := NewContentDetector(clues, 100)
	assert.True(t, detector.matches([]byte("and a needle in haystack")))
	assert.False(t, detector.matches([]byte("no match")))
}