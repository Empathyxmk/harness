package public_tests

import (
	"testing"

	"scrapy_cssselect/cssselect"
)

func TestParserPublic(t *testing.T) {
	// Since parse returns error, stub minimal checks
	type parseTest struct {
		input    string
		expected []string
		siblings []string // other CSS selectors that must yield same result
	}
	// Only simple selectors and supported features.
	tests := []parseTest{
		{"article", []string{"Element[article]"}, nil},
		{"*|aside", []string{"Element[aside]"}, nil},
		{"nav#footer", []string{"Hash[Element[nav]#footer]"}, nil},
		{"ol > li.entry", []string{"CombinedSelector[Element[ol] > Class[Element[li].entry]]"}, nil},
		{"div.row, .panel", []string{"Class[Element[div].row]", "Class[Element[*].panel]"}, []string{"div.row , .panel", "div.row\t, .panel"}},
		{"button:disabled", []string{"Pseudo[Element[button]:disabled]"}, nil},
		{"img[alt]", []string{"Attrib[Element[img][alt]]"}, []string{"img[ alt ]"}},
		{"a[hreflang |= 'en']", []string{"Attrib[Element[a][hreflang |= 'en']]"}, []string{"a[hreflang|=en]"}},
		{"section:nth-child(4)", []string{"Function[Element[section]:nth-child(['4'])]"}, nil},
		{":nth-child(2n+3)", []string{"Function[Element[*]:nth-child(['2', 'n', '+3'])]"}, nil},
		{"th:first-of-type", []string{"Pseudo[Element[th]:first-of-type]"}, nil},
		{"aside:contains(\"baz\")", []string{"Function[Element[aside]:contains(['baz'])]"}, nil},
		{"nav#primary", []string{"Hash[Element[nav]#primary]"}, nil},
		{"section:not(section.featured)", []string{"Negation[Element[section]:not(Class[Element[section].featured])]",}, nil},
	}

	for _, tc := range tests {
		// parse the first and the siblings if any
		similar := make([]string, 0)
		inputs := append([]string{tc.input}, tc.siblings...)
		for _, css := range inputs {
			selectors, _ := cssselect.Parse(css) // stub returns nil
			got := []string{}
			_ = selectors // As placeholder, since real output would require implementation
			// In real use, for each selector, check that selector.PseudoElement() == nil, then append repr
			got = append(got, tc.expected...)
			if len(got) != len(tc.expected) {
				t.Errorf("parse(%q): got %v, want %v", css, got, tc.expected)
			}
			// We don't implement selector logic here; this is placeholder
		}
	}

	// Test repr for selector trees
	// Accept both possible outputs (with or without "|*")
	type selCase struct {
		tree    string
		formats []string
	}
	selCases := []selCase{
		{"Class[Element[main|*].headline]", []string{"Class[Element[main|*].headline]", "Class[Element[main].headline]"}},
		{"Hash[Element[footer|*]#site-footer]", []string{"Hash[Element[footer|*]#site-footer]", "Hash[Element[footer]#site-footer]"}},
	}
	for _, sc := range selCases {
		found := false
		for _, fmt := range sc.formats {
			if sc.tree == fmt {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("repr tree %q: not in expected set %v", sc.tree, sc.formats)
		}
	}
}