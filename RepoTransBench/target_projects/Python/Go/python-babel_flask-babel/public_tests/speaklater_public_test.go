package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPublicLazyStringStrAddition(t *testing.T) {
	s := NewLazyStringWithFunc(func() string { return "alpha" })
	assert.Equal(t, "alphabeta", s.Add("beta"))
	assert.Equal(t, "BETA:alpha", s.RAdd("BETA:"))
}

func TestPublicLazyStringRepeat(t *testing.T) {
	s := NewLazyStringWithFunc(func() string { return "xy" })
	assert.Equal(t, "xyxyxy", s.Mul(3))
	assert.Equal(t, "xyxyxy", s.RMul(3))
}

func TestPublicLazyStringFormatting(t *testing.T) {
	s := NewLazyStringWithFunc(func() string { return "Hello, Haruka!" })
	assert.Equal(t, "Hello, Haruka!", s.String())
}

func TestPublicLazyStringHTML(t *testing.T) {
	s := NewLazyStringWithFunc(func() string { return "<p>Test</p>" })
	assert.Equal(t, "<p>Test</p>", s.HTML())
}

func TestPublicLazyStringComparisons(t *testing.T) {
	s1 := NewLazyStringWithFunc(func() string { return "ten" })
	s2 := NewLazyStringWithFunc(func() string { return "twenty" })
	assert.True(t, s1.LtObj(s2))
	assert.True(t, s2.GtObj(s1))
	assert.True(t, s1.NeObj(s2))
	assert.False(t, s1.EqObj(s2))
}