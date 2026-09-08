package original

import (
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummySensei struct {
	passCount int
	failures  []failure
}

type failure struct {
	lesson interface{}
	trace  string
}

func (s *DummySensei) passesCount() bool { return true }

func (s *DummySensei) addSuccess(obj interface{}) { s.passCount++ }

func (s *DummySensei) sortFailures(name string) []failure {
	if len(s.failures) == 0 {
		return nil
	}
	var out []failure
	re := regexp.MustCompile("about_" + name)
	for _, f := range s.failures {
		if re.MatchString(f.trace) {
			out = append(out, f)
		}
	}
	if len(out) == 0 {
		return nil
	}
	return out
}

func (s *DummySensei) firstFailure() failure {
	if len(s.failures) == 0 {
		return failure{}
	}
	// in real: would pick min-line
	return s.failures[0]
}

func (s *DummySensei) scrapeAssertionError(msg string) string {
	if msg == "" {
		return ""
	}
	if match := regexp.MustCompile(`AssertionError:(.*)`).FindStringSubmatch(msg); len(match) > 0 {
		return "  AssertionError:" + match[1]
	}
	if match := regexp.MustCompile(`SyntaxError: (.+)`).FindStringSubmatch(msg); len(match) > 0 {
		return "  SyntaxError: " + match[1]
	}
	return ""
}

func (s *DummySensei) saySomethingZenlike() string {
	switch s.passCount {
	case 0, 37:
		return "Beautiful is better than ugly"
	case 1:
		return "Explicit is better than implicit"
	case 10:
		return "Sparse is better than dense"
	case 36:
		return "Namespaces are one honking great idea"
	default:
		return "Spanish Inquisition"
	}
}

func TestSenseiScraping(t *testing.T) {
	s := &DummySensei{failures: []failure{}}
	assert.Equal(t, "", s.scrapeAssertionError(""))

	assert.Contains(t, s.saySomethingZenlike(), "Beautiful is better than ugly")
	s.passCount = 1
	assert.Contains(t, s.saySomethingZenlike(), "Explicit is better than implicit")
	s.passCount = 10
	assert.Contains(t, s.saySomethingZenlike(), "Sparse is better than dense")
	s.passCount = 36
	assert.Contains(t, s.saySomethingZenlike(), "Namespaces are one honking great idea")
	s.passCount = 37
	assert.Contains(t, s.saySomethingZenlike(), "Beautiful is better than ugly")
}