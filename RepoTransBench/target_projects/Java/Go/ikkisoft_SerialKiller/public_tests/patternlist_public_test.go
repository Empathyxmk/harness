package public_tests

import (
	"regexp"
	"testing"
)

func TestPatternMatchingWithNewPattern(t *testing.T) {
	patterns := []*regexp.Regexp{
		regexp.MustCompile(`^PUBLIC_\d+$`),
		regexp.MustCompile(`TestCase.*`),
	}
	value1 := "PUBLIC_1234"
	value2 := "TestCasePublic"
	value3 := "NotMatching"

	if !patterns[0].MatchString(value1) {
		t.Errorf("%q should match %q", value1, patterns[0].String())
	}
	if patterns[0].MatchString(value2) {
		t.Errorf("%q should NOT match %q", value2, patterns[0].String())
	}
	if !patterns[1].MatchString(value2) {
		t.Errorf("%q should match %q", value2, patterns[1].String())
	}
	if patterns[1].MatchString(value3) {
		t.Errorf("%q should NOT match %q", value3, patterns[1].String())
	}
}