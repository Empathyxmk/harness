package public_tests

import (
	"testing"
	"strings"
	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestAsciidammitPublic(t *testing.T) {
	s := "Café Noël Über ß"
	out := fuzzywuzzy.Asciidammit(s)
	assert.IsType(t, "", out)
	assert.NotContains(t, out, "\u00e9")
}

func TestAsciionlyPublic(t *testing.T) {
	in := fuzzywuzzy.Asciidammit("façade naïve jalapeño")
	out := fuzzywuzzy.Asciionly(in)
	for _, c := range out {
		assert.True(t, strings.ContainsRune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ", c))
	}
}

func TestFullProcessPublic(t *testing.T) {
	s := "Fußball & Crème brûlée"
	out := fuzzywuzzy.FullProcess(s, false)
	assert.IsType(t, "", out)
	assert.NotContains(t, out, "&")
}

func TestStringMatcherRatioPublic(t *testing.T) {
	s1 := "hello"
	s2 := "hullo"
	m := fuzzywuzzy.NewStringMatcher()
	m.SetSeq1(s1)
	m.SetSeq2(s2)
	ratio := m.Ratio()
	assert.True(t, ratio > 0.7)
	assert.True(t, ratio < 1.0)
}