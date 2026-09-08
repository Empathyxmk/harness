package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"gregmalcolm_python_koans/tests"
)

// Simulated port of Python's filter_koan_names (would typically be in a different package)
func filterKoanNames(infile string) []string {
	lines := strings.Split(infile, "\n")
	var out []string
	for _, s := range lines {
		trim := strings.TrimSpace(s)
		if len(trim) == 0 {
			continue
		}
		if strings.HasPrefix(trim, "#") {
			continue
		}
		out = append(out, trim)
	}
	return out
}

// Simulates koans_suite: returns class (testcase) names from fully qualified dot-names.
func koansSuite(names []string) []string {
	classes := make([]string, 0, len(names))
	for _, n := range names {
		parts := strings.Split(n, ".")
		if len(parts) > 0 {
			cls := parts[len(parts)-1]
			classes = append(classes, cls)
		}
	}
	return classes
}

func TestFilterKoanNames_EmptyInputProducesEmptyOutput(t *testing.T) {
	infile := ""
	expected := []string{}
	received := filterKoanNames(infile)
	assert.Equal(t, expected, received)
}

func TestFilterKoanNames_NamesYieldedExactlyAsInFile(t *testing.T) {
	names := []string{
		"this.is.a.test",
		"this.is.only.a.test",
	}
	infile := strings.Join(names, "\n")
	received := filterKoanNames(infile)
	assert.Equal(t, names, received)
}

func TestFilterKoanNames_WhitespaceIsStripped(t *testing.T) {
	names := []string{
		"this.is.a.test",
		"    white.space.should.be.stripped",
		"this.is.only.a.test",
		"white.space.should.be.stripped    ",
	}
	infile := strings.Join(names, "\n")
	expected := []string{
		"this.is.a.test",
		"white.space.should.be.stripped",
		"this.is.only.a.test",
		"white.space.should.be.stripped",
	}
	received := filterKoanNames(infile)
	assert.Equal(t, expected, received)
}

func TestFilterKoanNames_CommentedOutNamesAreExcluded(t *testing.T) {
	names := []string{
		"this.is.a.test",
		"#this.is.a.comment",
		"this.is.only.a.test",
		"    #    this.is.also a.comment    ",
	}
	infile := strings.Join(names, "\n")
	expected := []string{
		"this.is.a.test",
		"this.is.only.a.test",
	}
	received := filterKoanNames(infile)
	assert.Equal(t, expected, received)
}

func TestFilterKoanNames_AllBlankOrCommentLinesProduceEmptyOutput(t *testing.T) {
	names := []string{
		" ",
		"# This is a comment.",
		"\t",
		"    # This is also a comment.",
	}
	infile := strings.Join(names, "\n")
	expected := []string{}
	received := filterKoanNames(infile)
	assert.Equal(t, expected, received)
}

func TestKoansSuite_EmptyInputProducesEmptyTestsuite(t *testing.T) {
	names := []string{}
	// should return slice, not nil
	classes := koansSuite(names)
	assert.Empty(t, classes)
}

func TestKoansSuite_TestcaseNamesAppearInTestsuite(t *testing.T) {
	names := []string{
		"koans.about_asserts.AboutAsserts",
		"koans.about_none.AboutNone",
		"koans.about_strings.AboutStrings",
	}
	expected := []string{
		"AboutAsserts",
		"AboutNone",
		"AboutStrings",
	}
	classes := koansSuite(names)
	assert.ElementsMatch(t, expected, classes)
}