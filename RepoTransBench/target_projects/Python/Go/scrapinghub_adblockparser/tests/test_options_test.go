package tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestOptionSplitting(t *testing.T) {
	type splitCase struct {
		text   string
		result []string
	}
	cases := []splitCase{
		{"subdocument,third-party", []string{"subdocument", "third-party"}},
		{"object-subrequest,script,domain=~msnbc.msn.com,~www.nbcnews.com", []string{"object-subrequest", "script", "domain=~msnbc.msn.com,~www.nbcnews.com"}},
		{"~document,xbl,domain=~foo,bar,baz,~collapse,domain=foo.xbl|bar", []string{"~document", "xbl", "domain=~foo,bar,baz", "~collapse", "domain=foo.xbl|bar"}},
		{"domain=~example.com,foo.example.com,script", []string{"domain=~example.com,foo.example.com", "script"}},
	}

	for _, c := range cases {
		res := adblockparser.AdblockRule{}.SplitOptions(c.text)
		if !reflect.DeepEqual(res, c.result) {
			t.Errorf("For: %q\ngot %v\nwant %v", c.text, res, c.result)
		}
	}
}

func TestDomainParsing(t *testing.T) {
	type domCase struct {
		text   string
		result map[string]bool
	}
	cases := []domCase{
		{"domain=example.com", map[string]bool{"example.com": true}},
		{"domain=example.com|example.net", map[string]bool{"example.com": true, "example.net": true}},
		{"domain=~example.com", map[string]bool{"example.com": false}},
		{"domain=example.com|~foo.example.com", map[string]bool{"example.com": true, "foo.example.com": false}},
		{"domain=~foo.example.com|example.com", map[string]bool{"example.com": true, "foo.example.com": false}},
		{"domain=example.com,example.net", map[string]bool{"example.com": true, "example.net": true}},
		{"domain=example.com|~foo.example.com", map[string]bool{"example.com": true, "foo.example.com": false}},
		{"domain=~msnbc.msn.com,~www.nbcnews.com", map[string]bool{"msnbc.msn.com": false, "www.nbcnews.com": false}},
	}
	for _, c := range cases {
		got := adblockparser.AdblockRule{}.ParseDomainOption(c.text)
		if !reflect.DeepEqual(got, c.result) {
			t.Errorf("For: %q\ngot %v\nwant %v", c.text, got, c.result)
		}
	}
}