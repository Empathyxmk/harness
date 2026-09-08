package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestXPathFuncsHasClassSimple(t *testing.T) {
	body := `
        <p class="foo bar-baz">First</p>
        <p class="foo">Second</p>
        <p class="bar">Third</p>
        <p>Fourth</p>
        `
	sel := parsel.NewSelector(body)
	assert.ElementsMatch(t,
		[]string{"First", "Second"},
		sel.XPath(`//p[has-class("foo")]/text()`),
	)
	assert.ElementsMatch(t,
		[]string{"Third"},
		sel.XPath(`//p[has-class("bar")]/text()`),
	)
	assert.ElementsMatch(t,
		[]string{},
		sel.XPath(`//p[has-class("foo","bar")]/text()`),
	)
	assert.ElementsMatch(t,
		[]string{"First"},
		sel.XPath(`//p[has-class("foo","bar-baz")]/text()`),
	)
}

func TestXPathFuncsHasClassErrors(t *testing.T) {
	body := `<p CLASS="foo">First</p>`
	sel := parsel.NewSelector(body)
	_, err := sel.XPath(`has-class()`)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "at least 1 argument")

	_, err2 := sel.XPath(`has-class(.)`)
	assert.Error(t, err2)
	assert.Contains(t, err2.Error(), "must be strings")

	_, err3 := sel.XPath(`has-class("héllö")`)
	assert.Error(t, err3)
	assert.Contains(t, err3.Error(), "XML compatible")
}

func TestXPathFuncsHasClassUnicodeAndCaps(t *testing.T) {
	body := `<p CLASS="fóó">First</p>`
	sel := parsel.NewSelector(body)
	assert.ElementsMatch(t, []string{"First"}, sel.XPath(`//p[has-class("fóó")]/text()`))

	body2 := `<p CLASS="foo">First</p>`
	sel2 := parsel.NewSelector(body2)
	assert.ElementsMatch(t, []string{"First"}, sel2.XPath(`//p[has-class("foo")]/text()`))
}

func TestXPathFuncsHasClassNewlineAndTab(t *testing.T) {
	body := `<p CLASS="foo
        bar">First</p>`
	sel := parsel.NewSelector(body)
	assert.ElementsMatch(t, []string{"First"}, sel.XPath(`//p[has-class("foo")]/text()`))

	body2 := `<p CLASS="foo	bar">First</p>`
	sel2 := parsel.NewSelector(body2)
	assert.ElementsMatch(t, []string{"First"}, sel2.XPath(`//p[has-class("foo")]/text()`))
}

func TestXPathFuncsSetXPathFunc(t *testing.T) {
	myfuncCallCount := 0
	myfunc := func(ctx interface{}) error {
		myfuncCallCount++
		return nil
	}
	sel := parsel.NewSelector(`<p CLASS="foo">First</p>`)
	// Should fail because not registered
	_, err := sel.XPath("myfunc()")
	assert.Error(t, err)
	parsel.SetXPathFunc("myfunc", myfunc)
	_, err2 := sel.XPath("myfunc()")
	assert.NoError(t, err2)
	assert.Equal(t, 1, myfuncCallCount)
	parsel.SetXPathFunc("myfunc", nil)
	_, err3 := sel.XPath("myfunc()")
	assert.Error(t, err3)
}