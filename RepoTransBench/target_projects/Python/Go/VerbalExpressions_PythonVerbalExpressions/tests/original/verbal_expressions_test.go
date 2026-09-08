package original

import (
	"regexp"
	"testing"

	"verbalexpressions"
)

func TestShouldRenderVerExAsString(t *testing.T) {
	v := verbalexpressions.NewVerEx()
	v2 := v.Add("^$")
	if str := v2.String(); str != "^$" {
		t.Errorf("Expected '^$', got '%s'", str)
	}
}

func TestShouldRenderVerExListAsString(t *testing.T) {
	v := verbalexpressions.NewVerEx()
	v2 := v.Add([]string{"^", "[0-9]", "$"})
	if str := v2.String(); str != "^[0-9]$" {
		t.Errorf("Expected '^[0-9]$', got '%s'", str)
	}
}

func TestShouldMatchCharactersInRange(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Range("a", "c").Regex()
	for _, character := range []string{"a", "b", "c"} {
		if !exp.MatchString(character) {
			t.Errorf("Expected regex to match '%s'", character)
		}
	}
}

func TestShouldNotMatchCharactersOutsideOfRange(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Range("a", "c").Regex()
	if exp.MatchString("d") {
		t.Errorf("Expected regex to NOT match 'd'")
	}
}

func TestShouldMatchCharactersInExtendedRange(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Range("a", "b", "X", "Z").Regex()
	for _, character := range []string{"a", "b", "X", "Y", "Z"} {
		if !exp.MatchString(character) {
			t.Errorf("Expected to match '%s'", character)
		}
	}
}

func TestShouldNotMatchCharactersOutsideOfExtendedRange(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Range("a", "b", "X", "Z").Regex()
	for _, character := range []string{"c", "W"} {
		if exp.MatchString(character) {
			t.Errorf("Expected to NOT match '%s'", character)
		}
	}
}

func TestShouldMatchStartOfLine(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Regex()
	if !exp.MatchString("text  ") {
		t.Errorf("Expected regex to match 'text  ' (start-of-line)")
	}
}

func TestShouldMatchEndOfLine(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().EndOfLine().Regex()
	if !exp.MatchString("") {
		t.Errorf("Expected regex to match empty string at start and end-of-line")
	}
}

func TestShouldMatchAnything(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().EndOfLine().Regex()
	if !exp.MatchString("!@#$%¨&*()__+{}") {
		t.Errorf("Expected to match '!@#$%¨&*()__+{}'")
	}
}

func TestShouldMatchAnythingButSpecifiedElementWhenElementNotFound(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().AnythingBut("X").EndOfLine().Regex()
	if !exp.MatchString("Y Files") {
		t.Errorf("Expected to match 'Y Files' when 'X' is disallowed")
	}
}

func TestShouldNotMatchAnythingButSpecifiedElementWhenElementIsFound(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().AnythingBut("X").EndOfLine().Regex()
	if exp.MatchString("VerEX") {
		t.Errorf("Expected NOT to match 'VerEX' when 'X' is forbidden")
	}
}

func TestShouldFindElement(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Find("Wally").EndOfLine().Regex()
	if !exp.MatchString("Wally") {
		t.Errorf("Expected to match 'Wally'")
	}
}

func TestShouldNotFindMissingElement(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Find("Wally").EndOfLine().Regex()
	if exp.MatchString("Wall-e") {
		t.Errorf("Expected NOT to match 'Wall-e'")
	}
}

func TestShouldMatchWhenMaybeElementIsPresent(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Find("Python2.").Maybe("7").EndOfLine().Regex()
	if !exp.MatchString("Python2.7") {
		t.Errorf("Expected to match 'Python2.7'")
	}
}

func TestShouldMatchWhenMaybeElementIsMissing(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Find("Python2.").Maybe("7").EndOfLine().Regex()
	if !exp.MatchString("Python2.") {
		t.Errorf("Expected to match 'Python2.'")
	}
}

func TestShouldMatchOnAnyWhenElementIsFound(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Any("Q").Anything().EndOfLine().Regex()
	if !exp.MatchString("Query") {
		t.Errorf("Expected to match 'Query'")
	}
}

func TestShouldNotMatchOnAnyWhenElementIsNotFound(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Any("Q").Anything().EndOfLine().Regex()
	if exp.MatchString("W") {
		t.Errorf("Expected NOT to match 'W'")
	}
}

func TestShouldMatchWhenLineBreakPresent(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().LineBreak().Anything().EndOfLine().Regex()
	if !exp.MatchString("Marco \n Polo") {
		t.Errorf("Expected to match 'Marco \\n Polo'")
	}
}

func TestShouldMatchWhenLineBreakAndCarriageReturnPresent(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().LineBreak().Anything().EndOfLine().Regex()
	if !exp.MatchString("Marco \r\n Polo") {
		t.Errorf("Expected to match 'Marco \\r\\n Polo'")
	}
}

func TestShouldNotMatchWhenLineBreakIsMissing(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().LineBreak().Anything().EndOfLine().Regex()
	if exp.MatchString("Marco Polo") {
		t.Errorf("Expected NOT to match 'Marco Polo'")
	}
}

func TestShouldMatchWhenTabPresent(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Tab().EndOfLine().Regex()
	if !exp.MatchString("One tab only\t") {
		t.Errorf("Expected to match 'One tab only\\t'")
	}
}

func TestShouldNotMatchWhenTabIsMissing(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Tab().EndOfLine().Regex()
	if exp.MatchString("No tab here") {
		t.Errorf("Expected NOT to match 'No tab here'")
	}
}

func TestShouldMatchWhenWordPresent(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Word().EndOfLine().Regex()
	if !exp.MatchString("Oneword") {
		t.Errorf("Expected to match 'Oneword'")
	}
}

func TestNotMatchWhenTwoWordsArePresentInsteadOfOne(t *testing.T) {
	// This test is checking that tab is not present between two words, so shouldn't match
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Tab().EndOfLine().Regex()
	if exp.MatchString("Two words") {
		t.Errorf("Expected NOT to match 'Two words'")
	}
}

func TestShouldMatchWhenOrConditionFulfilled(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Find("G").Or().Find("h").EndOfLine().Regex()
	if !exp.MatchString("Github") {
		t.Errorf("Expected to match 'Github'")
	}
}

func TestShouldNotMatchWhenOrConditionNotFulfilled(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Find("G").Or().Find("h").EndOfLine().Regex()
	if exp.MatchString("Bitbucket") {
		t.Errorf("Expected NOT to match 'Bitbucket'")
	}
}

func TestShouldMatchOnUpperCaseWhenLowerCaseIsGivenAndAnyCaseIsTrue(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Find("THOR").EndOfLine().WithAnyCase(true).Regex()
	if !exp.MatchString("thor") {
		t.Errorf("Expected to match 'thor' with WithAnyCase(true)")
	}
}

func TestShouldMatchMultipleLines(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Anything().Find("Pong").Anything().EndOfLine().SearchOneLine(true).Regex()
	if !exp.MatchString("Ping \n Pong \n Ping") {
		t.Errorf("Expected to match with multiple lines")
	}
}

func TestShouldMatchEmailAddress(t *testing.T) {
	exp := verbalexpressions.NewVerEx().StartOfLine().Word().Then("@").Word().Then(".").Word().EndOfLine().Regex()
	if !exp.MatchString("mail@mail.com") {
		t.Errorf("Expected to match 'mail@mail.com'")
	}
}

func TestShouldMatchURL(t *testing.T) {
	exp := verbalexpressions.NewVerEx().
		StartOfLine().Then("http").Maybe("s").
		Then("://").Maybe("www.").Word().Then(".").Word().Maybe("/").EndOfLine().Regex()
	if !exp.MatchString("https://www.google.com/") {
		t.Errorf("Expected to match 'https://www.google.com/'")
	}
}