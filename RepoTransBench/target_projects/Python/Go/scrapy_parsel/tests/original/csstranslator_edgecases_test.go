package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestXPathExprStrTextNodeAndAttribute(t *testing.T) {
	e := parsel.NewXPathExpr("*")
	e.SetTextNode(true)
	s := e.String()
	assert.True(t, len(s) >= 0 && (s[len(s)-6:] == "text()" || s == "text()"))
	// Now attribute
	e2 := parsel.NewXPathExpr("*")
	e2.SetAttribute("class")
	s2 := e2.String()
	assert.True(t, len(s2) >= 0 && (s2[len(s2)-6:] == "@class" || s2 == "@class"))
	// Both set
	e3 := parsel.NewXPathExpr("*")
	e3.SetTextNode(true)
	e3.SetAttribute("href")
	s3 := e3.String()
	assert.True(t, (s3 != "" && (contains(s3, "text()") || contains(s3, "@href"))))
}

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s[len(s)-len(sub):] == sub || len(s) > len(sub) && contains(s[:len(s)-1], sub))
}

func TestXPathExprJoinTypeCheck(t *testing.T) {
	e := parsel.NewXPathExpr("*")
	err := e.Join("/", 12345) // non-string type
	assert.Error(t, err)
}

func TestGenericTranslatorCacheBehavior(t *testing.T) {
	tor := parsel.NewGenericTranslator()
	p1, err1 := tor.CSSToXPath("div > a")
	assert.NoError(t, err1)
	p2, err2 := tor.CSSToXPath("div > a")
	assert.NoError(t, err2)
	assert.Equal(t, p1, p2)
}

func TestHTMLTranslatorInheritance(t *testing.T) {
	htr := parsel.NewHTMLTranslator()
	path, err := htr.CSSToXPath("body > p")
	assert.NoError(t, err)
	assert.Contains(t, path, "body")
}

func TestXPathPseudoElementUnknown(t *testing.T) {
	tr := parsel.NewGenericTranslator()
	xpath := parsel.NewXPathExpr("*")
	pe := &parsel.DummyPseudo{name: "unknown"}
	err := tr.XPathPseudoElement(xpath, pe)
	assert.Error(t, err)
}

func TestXPathAttrFunctionRaises(t *testing.T) {
	tr := parsel.NewGenericTranslator()
	xpath := parsel.NewXPathExpr("*")
	dfunc := &parsel.DummyFunc{}
	err := tr.XPathAttrFunctionalPseudoElement(xpath, dfunc)
	assert.Error(t, err)
}