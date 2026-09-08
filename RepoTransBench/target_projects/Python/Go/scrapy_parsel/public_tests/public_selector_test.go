package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestExtractFromHTML(t *testing.T) {
	html := "<html><body><span>world</span></body></html>"
	sel := parsel.NewSelector(html)
	g := sel.XPath("//span/text()").Get()
	assert.Equal(t, "world", g)
}

func TestCssSelection(t *testing.T) {
	html := "<div><b>BoldContent</b></div>"
	sel := parsel.NewSelector(html)
	b := sel.CSS("b::text").Get()
	assert.Equal(t, "BoldContent", b)
}

func TestExtractFirstCustomDefault(t *testing.T) {
	html := "<root></root>"
	sel := parsel.NewSelector(html)
	get := sel.XPath("//missing/text()").GetDefault("nothing")
	assert.Equal(t, "nothing", get)
}

func TestExtractList(t *testing.T) {
	html := "<ul><li>egg</li><li>cheese</li></ul>"
	sel := parsel.NewSelector(html)
	result := sel.CSS("li::text").GetAll()
	assert.Equal(t, []string{"egg","cheese"}, result)
}

func TestErrorHandlingWrongType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic")
		}
	}()
	parsel.NewSelector(12345)
}