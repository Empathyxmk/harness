package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestJmespathJsonHasHtml(t *testing.T) {
	data := `{
			"content": [
				{"name":"A","value":"a"},
				{"name":{"age":18},"value":"b"},
				{"name":"C","value":"c"},
				{"name":"<a>D</a>","value":"<div>d</div>"}
			],
			"html": "<div><a>a<br>b</a>c</div><div><a>d</a>e<b>f</b></div>"
		}`
	sel := parsel.NewSelector(data)
	assert.Equal(t, "<div><a>a<br>b</a>c</div><div><a>d</a>e<b>f</b></div>", sel.Jmespath("html").Get())
	assert.ElementsMatch(t, []string{"a", "b", "d"}, sel.Jmespath("html").XPath("//div/a/text()"))
	assert.ElementsMatch(t, []string{"<b>f</b>"}, sel.Jmespath("html").CSS("div > b"))
	assert.Equal(t, 18, sel.Jmespath("content").Jmespath("name.age").Get())
}
func TestJmespathHtmlHasJson(t *testing.T) {
	htmlText := `<div>
		<h1>Information</h1>
		<content>
		{
		"user": [
				{"name":"A","age":18},
				{"name":"B","age":32},
				{"name":"C","age":22},
				{"name":"D","age":25}
		],
		"total":4,
		"status":"ok"
		}
		</content>
	</div>`
	sel := parsel.NewSelector(htmlText)
	assert.ElementsMatch(t, []string{"A","B","C","D"}, sel.XPath("//div/content/text()").Jmespath("user[*].name").GetAll())
	assert.ElementsMatch(t, []string{"A","B","C","D"}, sel.XPath("//div/content").Jmespath("user[*].name").GetAll())
	assert.Equal(t, 4, sel.XPath("//div/content").Jmespath("total").Get())
}
func TestJmespathWithRe(t *testing.T) {
	htmlText := `<div>
		<h1>Information</h1>
		<content>
		{
		"user": [
				{"name":"A","age":18},
				{"name":"B","age":32},
				{"name":"C","age":22},
				{"name":"D","age":25}
		],
		"total":4,
		"status":"ok"
		}
		</content>
	</div>`
	sel := parsel.NewSelector(htmlText)
	assert.ElementsMatch(t, []string{"A","B","C","D"}, sel.XPath("//div/content/text()").Jmespath("user[*].name").Re(`(\w+)`))
	assert.ElementsMatch(t, []string{"A","B","C","D"}, sel.XPath("//div/content").Jmespath("user[*].name").Re(`(\w+)`))

	_, err := sel.XPath("//div/content").Jmespath("user[*].age").ReErr(`(\d+)`)
	assert.Error(t, err)

	assert.ElementsMatch(t, []string{}, sel.XPath("//div/content").Jmespath("unavailable").Re(`(\d+)`))
	v := sel.XPath("//div/content").Jmespath("unavailable").ReFirst(`(\d+)`)
	assert.Nil(t, v)
	vals := sel.XPath("//div/content").Jmespath("user[*].age.to_string(@)").Re(`(\d+)`)
	assert.ElementsMatch(t, []string{"18","32","22","25"}, vals)
}

func TestJmespathJsonTypes(t *testing.T) {
	texts := []struct{
		text string
		root interface{}
	}{
		{"{}", map[string]interface{}{}},
		{`{"a":"b"}`, map[string]interface{}{"a": "b"}},
		{"[]", []interface{}{}},
		{`["a"]`, []interface{}{"a"}},
		{`""`, ""},
		{"0", 0},
		{"1", 1},
		{"true", true},
		{"false", false},
		{"null", nil},
	}
	for _, test := range texts {
		sel := parsel.NewSelectorWithRoot(test.text, test.root)
		assert.Equal(t, "json", sel.Type())
		assert.Equal(t, test.text, sel.Text())
		assert.EqualValues(t, test.root, sel.Root())

		sel2 := parsel.NewSelectorWithRoot("", test.root)
		assert.Equal(t, "json", sel2.Type())
		assert.EqualValues(t, test.root, sel2.Root())
	}
}