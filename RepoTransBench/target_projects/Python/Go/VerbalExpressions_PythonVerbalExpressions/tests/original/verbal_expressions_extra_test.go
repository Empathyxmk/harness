package original

import (
	"regexp"
	"testing"

	"verbalexpressions"
)

func TestAnything(t *testing.T) {
	v := verbalexpressions.NewVerEx().Anything()
	if v.Regex().FindString("abcdef") == "" {
		t.Errorf("Expected to match 'abcdef'")
	}
}

func TestAnythingBut(t *testing.T) {
	v := verbalexpressions.NewVerEx().AnythingBut("x")
	if v.Regex().FindString("abc") == "" {
		t.Errorf("Expected to match 'abc'")
	}
	if v.Regex().FindString("") == "" {
		t.Errorf("Expected to match empty string")
	}
	// Must not match a full string of only "x"
	if v.Regex().MatchString("x") {
		if v.Regex().FindString("x") == "x" && v.Regex().MatchString("x") {
			t.Errorf("Expected not to fullmatch 'x'")
		}
	}
	if v.Regex().FindString("abcdef") == "" {
		t.Errorf("Expected to match 'abcdef'")
	}
}

func TestEndOfLine(t *testing.T) {
	v := verbalexpressions.NewVerEx().EndOfLine()
	endReg := regexp.MustCompile(v.Source() + "$")
	if !endReg.MatchString("end$") {
		t.Errorf("Expected regex Source()+$ to match 'end$'")
	}
}

func TestMaybe(t *testing.T) {
	v := verbalexpressions.NewVerEx().Maybe("abc")
	if !v.Regex().MatchString("abc") {
		t.Errorf("Expected regex to match 'abc'")
	}
	if !v.Regex().MatchString("") {
		t.Errorf("Expected regex to match '' (empty string)")
	}
}

func TestStartOfLine(t *testing.T) {
	v := verbalexpressions.NewVerEx().StartOfLine()
	pattern := v.Source()
	if len(pattern) == 0 || pattern[0] != '^' {
		t.Errorf("Expected pattern to start with '^'")
	}
}

func TestFindAndThen(t *testing.T) {
	v := verbalexpressions.NewVerEx().Find("cat")
	if !v.Regex().MatchString("cat") {
		t.Errorf("Expected regex to match 'cat'")
	}
	v2 := verbalexpressions.NewVerEx().Then("dog")
	if !v2.Regex().MatchString("dog") {
		t.Errorf("Expected regex to match 'dog'")
	}
}

func TestAnyAnyOf(t *testing.T) {
	v := verbalexpressions.NewVerEx().Any("abc")
	if !v.Regex().MatchString("a") {
		t.Errorf("Expected regex to match 'a'")
	}
	if !v.Regex().MatchString("b") {
		t.Errorf("Expected regex to match 'b'")
	}
	if v.Regex().MatchString("d") {
		t.Errorf("Expected regex NOT to match 'd'")
	}
	v2 := verbalexpressions.NewVerEx().AnyOf("xyz")
	if !v2.Regex().MatchString("z") {
		t.Errorf("Expected regex to match 'z'")
	}
}

func TestLineBreakBr(t *testing.T) {
	v := verbalexpressions.NewVerEx().LineBreak()
	if !v.Regex().MatchString("\n") {
		t.Errorf("Expected regex to match '\\n'")
	}
	if !v.Regex().MatchString("\r\n") {
		t.Errorf("Expected regex to match '\\r\\n'")
	}
	v2 := verbalexpressions.NewVerEx().Br()
	if !v2.Regex().MatchString("\n") {
		t.Errorf("Expected regex to match '\\n'")
	}
}

func TestRangeWithOddArgs(t *testing.T) {
	v := verbalexpressions.NewVerEx().Range("a", "c", "0", "1")
	for _, s := range []string{"a", "b", "c", "0", "1"} {
		if !v.Regex().MatchString(s) {
			t.Errorf("Expected regex to match '%s'", s)
		}
	}
}

func TestTabAndWord(t *testing.T) {
	v := verbalexpressions.NewVerEx().Tab()
	if !v.Regex().MatchString("\t") {
		t.Errorf("Expected regex to match tab '\\t'")
	}
	w := verbalexpressions.NewVerEx().Word()
	if !w.Regex().MatchString("wordtest") {
		t.Errorf("Expected regex to match 'wordtest', got false")
	}
}

func TestOrWithoutValue(t *testing.T) {
	v := verbalexpressions.NewVerEx().Find("foo").Or()
	if found := v.Source(); found == "" || !contains(found, "|") {
		t.Errorf("Expected regex source to contain '|'")
	}
	// In Go, the method exists - so just check it, no hasattr needed.
}

func TestOrWithValue(t *testing.T) {
	v := verbalexpressions.NewVerEx().Find("foo").Or("bar")
	if found := v.Source(); !contains(found, "|(bar)") {
		t.Errorf("Expected regex source to contain '|(bar)'")
	}
}

func TestReplace(t *testing.T) {
	v := verbalexpressions.NewVerEx().Find("foo")
	result := v.Replace("foofoo", "bar")
	if result != "barbar" {
		t.Errorf("Expected replaced result to be 'barbar', got '%s'", result)
	}
}

func TestWithAnyCase(t *testing.T) {
	v := verbalexpressions.NewVerEx().Find("abc").WithAnyCase(true)
	if !v.HasModifier('i') {
		t.Errorf("Expected 'i' modifier for WithAnyCase(true)")
	}
	v.WithAnyCase(false)
	if v.HasModifier('i') {
		t.Errorf("Expected NOT to have 'i' modifier for WithAnyCase(false)")
	}
}

func TestSearchOneLine(t *testing.T) {
	v := verbalexpressions.NewVerEx().SearchOneLine(true)
	if !v.HasModifier('m') {
		t.Errorf("Expected 'm' modifier for SearchOneLine(true)")
	}
	v.SearchOneLine(false)
	if v.HasModifier('m') {
		t.Errorf("Expected NOT to have 'm' modifier for SearchOneLine(false)")
	}
}

func TestWithAscii(t *testing.T) {
	v := verbalexpressions.NewVerEx().WithAscii(true)
	if !v.HasModifier('a') {
		t.Errorf("Expected 'a' modifier for WithAscii(true)")
	}
	v.WithAscii(false)
	if v.HasModifier('a') {
		t.Errorf("Expected NOT to have 'a' modifier for WithAscii(false)")
	}
}

func TestValueAndSource(t *testing.T) {
	v := verbalexpressions.NewVerEx().Find("cat")
	if v.Value() != v.Source() {
		t.Errorf("Expected Value() == Source() but got %s vs %s", v.Value(), v.Source())
	}
	if v.Raw() != v.Source() {
		t.Errorf("Expected Raw() == Source() but got %s vs %s", v.Raw(), v.Source())
	}
}

// --- Helpers

func contains(s, substr string) bool {
	return regexp.MustCompile(regexp.QuoteMeta(substr)).FindString(s) != ""
}