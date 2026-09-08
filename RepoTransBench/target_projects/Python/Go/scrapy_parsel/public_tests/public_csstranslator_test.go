package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestGenericTranslatorCacheBehaviorPublic(t *testing.T) {
	g := parsel.NewGenericTranslator()
	result, err := g.CSSToXPath("a#main.class")
	assert.NoError(t, err)
	assert.Equal(t, `//a[contains(concat(" ",normalize-space(@class)," ")," class ")][@id = "main"]`, result)
	result2, err2 := g.CSSToXPath("a#main.class")
	assert.NoError(t, err2)
	assert.Equal(t, result, result2)
}

func TestHTMLTranslatorInheritancePublic(t *testing.T) {
	assert.True(t, parsel.HTMLTranslatorIsGenericTranslator())
}

func TestXPathExprJoinTypeCheckPublic(t *testing.T) {
	g := parsel.NewGenericTranslator()
	err := g.XPathExprJoin("span", 123)
	assert.Error(t, err)
}

func TestXPathPseudoElementUnknownPublic(t *testing.T) {
	g := parsel.NewGenericTranslator()
	_, err := g.CSSToXPath("a::unknown")
	assert.Error(t, err)
}