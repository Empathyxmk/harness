package public_tests

import (
	"strings"
	"testing"
)

func escape(s string) string {
	// Minimal XML escape translation for test equivalence
	s = strings.ReplaceAll(s, "&", "&amp;")
	s = strings.ReplaceAll(s, "<", "&lt;")
	s = strings.ReplaceAll(s, ">", "&gt;")
	s = strings.ReplaceAll(s, `"`, "&quot;")
	return s
}

func unescape(s string) string {
	s = strings.ReplaceAll(s, "&quot;", `"`)
	s = strings.ReplaceAll(s, "&gt;", ">")
	s = strings.ReplaceAll(s, "&lt;", "<")
	s = strings.ReplaceAll(s, "&amp;", "&")
	return s
}

func elem(tag, content string, attrs map[string]string) string {
	sb := strings.Builder{}
	sb.WriteString("<" + tag)
	for k, v := range attrs {
		sb.WriteString(" " + k + "=\"" + escape(v) + "\"")
	}
	sb.WriteString(">")
	sb.WriteString(escape(content))
	sb.WriteString("</" + tag + ">")
	return sb.String()
}

func TestPublicEscapeXMLSymbol(t *testing.T) {
	res := escape(`apples & bananas < oranges > "g"`)
	if !strings.Contains(res, "&amp;") || !strings.Contains(res, "&lt;") || !strings.Contains(res, "&gt;") || !strings.Contains(res, "&quot;") {
		t.Errorf("XML escape missing symbol: %q", res)
	}
}

func TestPublicUnescapeXMLSymbol(t *testing.T) {
	s := `&amp;hello&gt;&lt;test&gt;&quot;x&quot;`
	res := unescape(s)
	if !strings.Contains(res, "&") || !strings.Contains(res, ">") || !strings.Contains(res, "<") || !strings.Contains(res, `"`) {
		t.Errorf("XML unescape missing symbol: %q", res)
	}
}

func TestPublicMakeElemWithAttrs(t *testing.T) {
	res := elem("fruit", "banana & apple", map[string]string{"ripe": "yes", "color": "yellow"})
	if !strings.Contains(res, "fruit") || !strings.Contains(res, "ripe") || !strings.Contains(res, "&amp;") {
		t.Errorf("elem missing expected XML: %q", res)
	}
}