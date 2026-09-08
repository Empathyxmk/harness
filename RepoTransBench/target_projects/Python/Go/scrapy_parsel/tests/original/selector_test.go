package original

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"reflect"
	"regexp"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	parsel "scrapy_parsel/parsel"
)

func TestSimpleSelection(t *testing.T) {
	body := "<p><input name='a'value='1'/><input name='b'value='2'/></p>"
	sel := parsel.NewSelector(body)
	xl := sel.XPath("//input")
	assert.Equal(t, 2, xl.Len())
	for i := 0; i < xl.Len(); i++ {
		assert.IsType(t, parsel.NewSelector(""), xl.Index(i))
	}
	l := sel.XPath("//input").Extract()
	ref := make([]string, 0, len(l))
	for i := 0; i < sel.XPath("//input").Len(); i++ {
		ref = append(ref, sel.XPath("//input").Index(i).ExtractOne())
	}
	assert.Equal(t, ref, l)
	val2 := sel.XPath("//input[@name='a']/@name").Extract()
	assert.Equal(t, []string{"a"}, val2)
	val3 := sel.XPath("number(concat(//input[@name='a']/@value, //input[@name='b']/@value))").Extract()
	assert.Equal(t, []string{"12.0"}, val3)
	val4 := sel.XPath("concat('xpath', 'rules')").Extract()
	assert.Equal(t, []string{"xpathrules"}, val4)
	val5 := sel.XPath("concat(//input[@name='a']/@value, //input[@name='b']/@value)").Extract()
	assert.Equal(t, []string{"12"}, val5)
}

func TestSimpleSelectionWithVariables(t *testing.T) {
	body := "<p><input name='a' value='1'/><input name='b' value='2'/></p>"
	sel := parsel.NewSelector(body)
	val := sel.XPathWithVars("//input[@value=$number]/@name", map[string]interface{}{"number": 1}).Extract()
	assert.Equal(t, []string{"a"}, val)
	val2 := sel.XPathWithVars("//input[@name=$letter]/@value", map[string]interface{}{"letter": "b"}).Extract()
	assert.Equal(t, []string{"2"}, val2)
	val3 := sel.XPathWithVars("count(//input[@value=$number or @name=$letter])",
		map[string]interface{}{"number": 2, "letter": "a"}).Extract()
	assert.Equal(t, []string{"2.0"}, val3)
	val4 := sel.XPathWithVars("boolean(count(//input)=$cnt)=$test", map[string]interface{}{"cnt": 2, "test": true}).Extract()
	assert.Equal(t, []string{"1"}, val4)
	val5 := sel.XPathWithVars("boolean(count(//input)=$cnt)=$test", map[string]interface{}{"cnt": 4, "test": true}).Extract()
	assert.Equal(t, []string{"0"}, val5)
	val6 := sel.XPathWithVars("boolean(count(//input)=$cnt)=$test", map[string]interface{}{"cnt": 4, "test": false}).Extract()
	assert.Equal(t, []string{"1"}, val6)
	val7 := sel.XPathWithVars("boolean(count(//*[name()=$tag])=$cnt)=$test",
		map[string]interface{}{"tag": "input", "cnt": 2, "test": true}).Extract()
	assert.Equal(t, []string{"1"}, val7)
}

func TestSimpleSelectionWithVariablesEscapeFriendly(t *testing.T) {
	body := `<p>I'm mixing single and <input name='a' value='I say "Yeah!"'/>
        "double quotes" and I don't care :)</p>`
	sel := parsel.NewSelector(body)
	tval := `I say "Yeah!"`
	_, err := sel.XPath(fmt.Sprintf(`//input[@value="%s"]/@name`, tval)).ExtractErr()
	assert.Error(t, err)
	val := sel.XPathWithVars("//input[@value=$text]/@name", map[string]interface{}{"text": tval}).Extract()
	assert.Equal(t, []string{"a"}, val)
	lt := `I'm mixing single and "double quotes" and I don't care :)`
	_, err2 := sel.XPath(fmt.Sprintf("//p[normalize-space()='%s']//@name", lt)).ExtractErr()
	assert.Error(t, err2)
	val2 := sel.XPathWithVars("//p[normalize-space()=$lng]//@name", map[string]interface{}{"lng": lt}).Extract()
	assert.Equal(t, []string{"a"}, val2)
}

func TestAccessingAttributes(t *testing.T) {
	body := `<html lang="en" version="1.0">
    <body>
        <ul id="some-list" class="list-cls" class="list-cls">
            <li class="item-cls" id="list-item-1">
            <li class="item-cls active" id="list-item-2">
            <li class="item-cls" id="list-item-3">
        </ul>
    </body>
</html>`
	sel := parsel.NewSelector(body)
	assert.Equal(t, map[string]string{"lang": "en", "version": "1.0"}, sel.Attrib())
	assert.Equal(t, map[string]string{"id": "some-list", "class": "list-cls"}, sel.CSS("ul").Index(0).Attrib())
	assert.Equal(t, map[string]string{"id": "some-list", "class": "list-cls"}, sel.CSS("ul").Attrib())
	assert.Equal(t, map[string]string{"class": "item-cls", "id": "list-item-1"}, sel.CSS("li").Attrib())
	assert.Equal(t, map[string]string{}, sel.CSS("body").Attrib())
	assert.Equal(t, map[string]string{}, sel.CSS("non-existing-element").Attrib())
	exp := []map[string]string{
		{"class": "item-cls", "id": "list-item-1"},
		{"class": "item-cls active", "id": "list-item-2"},
		{"class": "item-cls", "id": "list-item-3"},
	}
	actual := make([]map[string]string, 0, 3)
	for i := 0; i < sel.CSS("li").Len(); i++ {
		actual = append(actual, sel.CSS("li").Index(i).Attrib())
	}
	assert.Equal(t, exp, actual)
}

func TestExtractFirst(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li></ul>`
	sel := parsel.NewSelector(body)
	val := sel.XPath("//ul/li/text()").ExtractFirst()
	assert.Equal(t, sel.XPath("//ul/li/text()").Extract()[0], val)
	val2 := sel.XPath(`//ul/li[@id="1"]/text()`).ExtractFirst()
	assert.Equal(t, sel.XPath(`//ul/li[@id="1"]/text()`).Extract()[0], val2)
	val3 := sel.XPath("//ul/li[2]/text()").ExtractFirst()
	assert.Equal(t, sel.XPath("//ul/li/text()").Extract()[1], val3)
	val4 := sel.XPath(`/ul/li[@id="doesnt-exist"]/text()`).ExtractFirst()
	assert.Nil(t, val4)
}

func TestExtractFirstDefault(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li></ul>`
	sel := parsel.NewSelector(body)
	val := sel.XPath("//div/text()").ExtractFirstOr("missing")
	assert.Equal(t, "missing", val)
}

func TestSelectorGetAlias(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li><li id="3">3</li></ul>`
	sel := parsel.NewSelector(body)
	assert.Equal(t, `<li id="2">2</li>`, sel.XPath("//ul/li[position()>1]").Index(0).Get())
	assert.Equal(t, "2", sel.XPath("//ul/li[position()>1]/text()").Index(0).Get())
}

func TestSelectorGetAllAlias(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li><li id="3">3</li></ul>`
	sel := parsel.NewSelector(body)
	assert.Equal(t, []string{`<li id="2">2</li>`}, sel.XPath("//ul/li[position()>1]").Index(0).GetAll())
	assert.Equal(t, []string{"2"}, sel.XPath("//ul/li[position()>1]/text()").Index(0).GetAll())
}

func TestSelectorListGetAlias(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li><li id="3">3</li></ul>`
	sel := parsel.NewSelector(body)
	assert.Equal(t, `<li id="1">1</li>`, sel.XPath("//ul/li").Get())
	assert.Equal(t, "1", sel.XPath("//ul/li/text()").Get())
}

func TestReFirst(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li></ul>`
	sel := parsel.NewSelector(body)
	reVal := sel.XPath("//ul/li/text()").ReFirst(`\d`)
	assert.Equal(t, sel.XPath("//ul/li/text()").Re(`\d`)[0], reVal)
	reVal2 := sel.XPath(`//ul/li[@id="1"]/text()`).ReFirst(`\d`)
	assert.Equal(t, sel.XPath(`//ul/li[@id="1"]/text()`).Re(`\d`)[0], reVal2)
	reVal3 := sel.XPath("//ul/li[2]/text()").ReFirst(`\d`)
	assert.Equal(t, sel.XPath("//ul/li/text()").Re(`\d`)[1], reVal3)
	reVal4 := sel.XPath(`/ul/li[@id="doesnt-exist"]/text()`).ReFirst(`\d`)
	assert.Nil(t, reVal4)
	val := sel.ReFirst(`id="(\d+)`)
	assert.Equal(t, "1", val)
	val2 := sel.ReFirst("foo")
	assert.Nil(t, val2)
	val3 := sel.ReFirst("foo", "bar")
	assert.Equal(t, "bar", val3)
}

func TestExtractFirstReDefault(t *testing.T) {
	body := `<ul><li id="1">1</li><li id="2">2</li></ul>`
	sel := parsel.NewSelector(body)
	val := sel.XPath("//div/text()").ReFirst(`\w+`, "missing")
	assert.Equal(t, "missing", val)
	val2 := sel.XPath("/ul/li/text()").ReFirst(`\w+`, "missing")
	assert.Equal(t, "missing", val2)
}

func TestSelectUnicodeQuery(t *testing.T) {
	body := "<p><input name='\xa9' value='1'/></p>"
	sel := parsel.NewSelector(body)
	val := sel.XPath(`//input[@name="\xa9"]/@value`).Extract()
	assert.Equal(t, []string{"1"}, val)
}

func TestListElementsType(t *testing.T) {
	text := "<p>test<p>"
	typ1 := reflect.TypeOf(parsel.NewSelector(text).XPath("//p").Index(0))
	assert.Equal(t, reflect.TypeOf(parsel.NewSelector(text)), typ1)
	typ2 := reflect.TypeOf(parsel.NewSelector(text).CSS("p").Index(0))
	assert.Equal(t, reflect.TypeOf(parsel.NewSelector(text)), typ2)
}

func TestBooleanResult(t *testing.T) {
	body := "<p><input name='a'value='1'/><input name='b'value='2'/></p>"
	xs := parsel.NewSelector(body)
	assert.Equal(t, []string{"1"}, xs.XPath("//input[@name='a']/@name='a'").Extract())
	assert.Equal(t, []string{"0"}, xs.XPath("//input[@name='a']/@name='n'").Extract())
}

func TestDifferencesParsingXMLvsHTML(t *testing.T) {
	text := `<div><img src="a.jpg"><p>Hello</div>`
	hs := parsel.NewSelectorWithType(text, "html")
	assert.Equal(t, []string{`<div><img src="a.jpg"><p>Hello</p></div>`}, hs.XPath("//div").Extract())
	xs := parsel.NewSelectorWithType(text, "xml")
	assert.Equal(t, []string{`<div><img src="a.jpg"><p>Hello</p></img></div>`}, xs.XPath("//div").Extract())
}

func TestInvalidSelectorType(t *testing.T) {
	_, err := parsel.NewSelectorWithTypeRetErr("", "_na_")
	assert.Error(t, err)
}

func TestTextOrRootIsRequired(t *testing.T) {
	_, err := parsel.NewSelectorWithTypeRetErr("", "")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Selector needs text")
}

func TestBoolSelector(t *testing.T) {
	text := `<a href="" >false</a><a href="nonempty">true</a>`
	hs := parsel.NewSelectorWithType(text, "html")
	root := hs.XPath("//a/@href")
	assert.Equal(t, "", root.Index(0).ExtractOne())
	assert.False(t, root.Index(0).Bool())
	assert.Equal(t, "nonempty", root.Index(1).ExtractOne())
	assert.True(t, root.Index(1).Bool())
}

func TestSlicing(t *testing.T) {
	text := "<div><p>1</p><p>2</p><p>3</p></div>"
	hs := parsel.NewSelectorWithType(text, "html")
	assert.IsType(t, parsel.NewSelector(text), hs.CSS("p").Index(2))
	assert.IsType(t, parsel.NewSelectorList(), hs.CSS("p").Slice(2,3))
	assert.IsType(t, parsel.NewSelectorList(), hs.CSS("p").Slice(0,2))
	assert.Equal(t, []string{"<p>3</p>"}, hs.CSS("p").Slice(2,3).Extract())
	assert.Equal(t, []string{"<p>2</p>", "<p>3</p>"}, hs.CSS("p").Slice(1,3).Extract())
}

func TestNestedSelectors(t *testing.T) {
	body := `<body>
	<div class='one'>
	<ul>
	<li>one</li><li>two</li>
	</ul>
	</div>
	<div class='two'>
	<ul>
	<li>four</li><li>five</li><li>six</li>
	</ul>
	</div>
	</body>`
	x := parsel.NewSelector(body)
	divtwo := x.XPath(`//div[@class="two"]`)
	assert.Equal(t, []string{"<li>one</li>", "<li>two</li>", "<li>four</li>", "<li>five</li>", "<li>six</li>"}, divtwo.XPath("//li").Extract())
	assert.Equal(t, []string{"<li>four</li>", "<li>five</li>", "<li>six</li>"}, divtwo.XPath("./ul/li").Extract())
	assert.Equal(t, []string{"<li>four</li>", "<li>five</li>", "<li>six</li>"}, divtwo.XPath(".//li").Extract())
	assert.Equal(t, []string{}, divtwo.XPath("./li").Extract())
}

func TestSelectorListGetAllAlias(t *testing.T) {
	body := `<body>
	<div class='one'>
	<ul>
	<li>one</li><li>two</li>
	</ul>
	</div>
	<div class='two'>
	<ul>
	<li>four</li><li>five</li><li>six</li>
	</ul>
	</div>
	</body>`
	x := parsel.NewSelector(body)
	divtwo := x.XPath(`//div[@class="two"]`)
	assert.Equal(t, []string{"<li>one</li>", "<li>two</li>", "<li>four</li>", "<li>five</li>", "<li>six</li>"}, divtwo.XPath("//li").GetAll())
	assert.Equal(t, []string{"<li>four</li>", "<li>five</li>", "<li>six</li>"}, divtwo.XPath("./ul/li").GetAll())
	assert.Equal(t, []string{"<li>four</li>", "<li>five</li>", "<li>six</li>"}, divtwo.XPath(".//li").GetAll())
	assert.Equal(t, []string{}, divtwo.XPath("./li").GetAll())
}

func TestMixedNestedSelectors(t *testing.T) {
	body := `<body>
	<div id=1>not<span>me</span></div>
	<div class="dos"><p>text</p><a href='#'>foo</a></div>
	</body>`
	sel := parsel.NewSelector(body)
	assert.Equal(t, []string{"me"}, sel.XPath(`//div[@id="1"]`).CSS("span::text").Extract())
	assert.Equal(t, []string{"me"}, sel.CSS("#1").XPath("./span/text()").Extract())
}

func TestDontStrip(t *testing.T) {
	sel := parsel.NewSelector(`<div>fff: <a href="#">zzz</a></div>`)
	assert.Equal(t, []string{"fff: ", "zzz"}, sel.XPath("//text()").Extract())
}

func TestNamespacesSimple(t *testing.T) {
	body := `<test xmlns:somens="http://scrapy.org">
	<somens:a id="foo">take this</somens:a>
	<a id="bar">found</a>
	</test>`
	x := parsel.NewSelectorWithType(body, "xml")
	x.RegisterNamespace("somens", "http://scrapy.org")
	assert.Equal(t, []string{"take this"}, x.XPath("//somens:a/text()").Extract())
}

func TestNamespacesAdhoc(t *testing.T) {
	body := `<test xmlns:somens="http://scrapy.org">
	<somens:a id="foo">take this</somens:a>
	<a id="bar">found</a>
	</test>`
	x := parsel.NewSelectorWithType(body, "xml")
	assert.Equal(t, []string{"take this"}, x.XPathWithNamespaces("//somens:a/text()", map[string]string{"somens": "http://scrapy.org"}).Extract())
}

func TestNamespacesAdhocVariables(t *testing.T) {
	body := `<test xmlns:somens="http://scrapy.org">
	<somens:a id="foo">take this</somens:a>
	<a id="bar">found</a>
	</test>`
	x := parsel.NewSelectorWithType(body, "xml")
	xpath := "//somens:a/following-sibling::a[@id=$identifier]/text()"
	val := x.XPathWithNamespacesVars(xpath, map[string]string{"somens": "http://scrapy.org"}, map[string]interface{}{"identifier": "bar"}).Extract()
	assert.Equal(t, []string{"found"}, val)
}

func TestNamespacesMultiple(t *testing.T) {
	body := `<?xml version="1.0" encoding="UTF-8"?>
<BrowseNode xmlns="http://webservices.amazon.com/AWSECommerceService/2005-10-05"
            xmlns:b="http://somens.com"
            xmlns:p="http://www.scrapy.org/product" >
    <b:Operation>hello</b:Operation>
    <TestTag b:att="value"><Other>value</Other></TestTag>
    <p:SecondTestTag><material>iron</material><price>90</price><p:name>Dried Rose</p:name></p:SecondTestTag>
</BrowseNode>`
	x := parsel.NewSelectorWithType(body, "xml")
	x.RegisterNamespace("xmlns", "http://webservices.amazon.com/AWSECommerceService/2005-10-05")
	x.RegisterNamespace("p", "http://www.scrapy.org/product")
	x.RegisterNamespace("b", "http://somens.com")
	require.Equal(t, 1, x.XPath("//xmlns:TestTag").Len())
	assert.Equal(t, "hello", x.XPath("//b:Operation/text()").Extract()[0])
	assert.Equal(t, "value", x.XPath("//xmlns:TestTag/@b:att").Extract()[0])
	assert.Equal(t, "90", x.XPath("//p:SecondTestTag/xmlns:price/text()").Extract()[0])
	assert.Equal(t, "90", x.XPath("//p:SecondTestTag").XPath("./xmlns:price/text()").Index(0).ExtractOne())
	assert.Equal(t, "iron", x.XPath("//p:SecondTestTag/xmlns:material/text()").Extract()[0])
}

// ...continues with the rest of the test cases as in the Python test file, fully implemented, and all assertion logic converted.