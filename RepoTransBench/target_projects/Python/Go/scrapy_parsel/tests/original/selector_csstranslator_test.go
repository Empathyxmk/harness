package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	//"github.com/antchfx/htmlquery" // When parsing HTML fragments
	parsel "scrapy_parsel/parsel"
)

func TestHTMLTranslatorAttrFunction(t *testing.T) {
	tr := parsel.NewHTMLTranslator()
	tests := []struct{
		css string
		xpath string
	}{
		{"::attr(name)", "descendant-or-self::*/@name"},
		{"a::attr(href)", "descendant-or-self::a/@href"},
		{"a ::attr(img)", "descendant-or-self::a/descendant-or-self::*/@img"},
		{"a > ::attr(class)", "descendant-or-self::a/*/@class"},
	}
	for _, test := range tests {
		actual, err := tr.CSSToXPath(test.css)
		require.NoError(t, err, test.css)
		assert.Equal(t, test.xpath, actual, test.css)
	}
}

func TestHTMLTranslatorAttrFunctionException(t *testing.T) {
	tr := parsel.NewHTMLTranslator()
	errorTests := []struct{
		css string
		expectedErr string // match by error message fragment
	}{
		{"::attr(12)", "expression error"},
		{"::attr(34test)", "expression error"},
		{"::attr(@href)", "syntax error"},
	}
	for _, test := range errorTests {
		_, err := tr.CSSToXPath(test.css)
		assert.Error(t, err, test.css)
		assert.Contains(t, err.Error(), test.expectedErr, test.css)
	}
}

func TestHTMLTranslatorTextPseudoElement(t *testing.T) {
	tr := parsel.NewHTMLTranslator()
	tests := []struct{
		css string
		xpath string
	}{
		{"::text", "descendant-or-self::text()"},
		{"p::text", "descendant-or-self::p/text()"},
		{"p ::text", "descendant-or-self::p/descendant-or-self::text()"},
		{"#id::text", "descendant-or-self::*[@id = 'id']/text()"},
		{"p#id::text", "descendant-or-self::p[@id = 'id']/text()"},
		{"p#id ::text", "descendant-or-self::p[@id = 'id']/descendant-or-self::text()"},
		{"p#id > ::text", "descendant-or-self::p[@id = 'id']/*/text()"},
		{"p#id ~ ::text", "descendant-or-self::p[@id = 'id']/following-sibling::*/text()"},
		{"a[href]::text", "descendant-or-self::a[@href]/text()"},
		{"a[href] ::text", "descendant-or-self::a[@href]/descendant-or-self::text()"},
		{"p::text, a::text", "descendant-or-self::p/text() | descendant-or-self::a/text()"},
	}
	for _, test := range tests {
		actual, err := tr.CSSToXPath(test.css)
		require.NoError(t, err, test.css)
		assert.Equal(t, test.xpath, actual, test.css)
	}
}

func TestHTMLTranslatorPseudoFunctionException(t *testing.T) {
	tr := parsel.NewHTMLTranslator()
	errorTests := []struct{
		css string
		expectedErr string // error fragment
	}{
		{"::attribute(12)", "expression error"},
		{"::text()", "expression error"},
		{"::attr(@href)", "syntax error"},
	}
	for _, test := range errorTests {
		_, err := tr.CSSToXPath(test.css)
		assert.Error(t, err, test.css)
		assert.Contains(t, err.Error(), test.expectedErr, test.css)
	}
}

func TestHTMLTranslatorUnknownPseudoElement(t *testing.T) {
	tr := parsel.NewHTMLTranslator()
	_, err := tr.CSSToXPath("::text-node")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "expression error")
}

func TestHTMLTranslatorUnknownPseudoClass(t *testing.T) {
	tr := parsel.NewHTMLTranslator()
	errorCases := []string{":text", ":attribute(name)"}
	for _, css := range errorCases {
		_, err := tr.CSSToXPath(css)
		assert.Error(t, err, css)
		assert.Contains(t, err.Error(), "expression error")
	}
}

// Test the generic translator as well
func TestGenericTranslatorAttrFunction(t *testing.T) {
	tr := parsel.NewGenericTranslator()
	tests := []struct{
		css string
		xpath string
	}{
		{"::attr(name)", "descendant-or-self::*/@name"},
		{"a::attr(href)", "descendant-or-self::a/@href"},
		{"a ::attr(img)", "descendant-or-self::a/descendant-or-self::*/@img"},
		{"a > ::attr(class)", "descendant-or-self::a/*/@class"},
	}
	for _, test := range tests {
		actual, err := tr.CSSToXPath(test.css)
		require.NoError(t, err, test.css)
		assert.Equal(t, test.xpath, actual, test.css)
	}
}

func TestGenericTranslatorAttrFunctionException(t *testing.T) {
	tr := parsel.NewGenericTranslator()
	errorTests := []struct{
		css string
		expectedErr string // match by error message fragment
	}{
		{"::attr(12)", "expression error"},
		{"::attr(34test)", "expression error"},
		{"::attr(@href)", "syntax error"},
	}
	for _, test := range errorTests {
		_, err := tr.CSSToXPath(test.css)
		assert.Error(t, err, test.css)
		assert.Contains(t, err.Error(), test.expectedErr, test.css)
	}
}

func TestUtilCss2XPath(t *testing.T) {
	expected := "descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' some-class ')]"
	result, err := parsel.CsstoXPath(".some-class")
	require.NoError(t, err)
	assert.Equal(t, expected, result)
}