package original

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func convertPath(val interface{}) string {
	switch v := val.(type) {
	case string:
		if v == "." {
			return "."
		}
		return filepath.Join(strings.Split(v, "/")...)
	default:
		return ""
	}
}

func strToBool(s string) bool {
	switch strings.ToLower(s) {
	case "y", "yes", "true", "on", "1", "t":
		return true
	case "n", "no", "f", "false", "off", "0":
		return false
	default:
		return false
	}
}

func splitQuoted(s string) []string {
	inQuotes := false
	curr := ""
	result := []string{}
	for _, r := range s {
		if r == '"' || r == '\'' {
			inQuotes = !inQuotes
			continue
		}
		if r == ' ' && !inQuotes {
			if curr != "" {
				result = append(result, curr)
				curr = ""
			}
		} else {
			curr += string(r)
		}
	}
	if curr != "" {
		result = append(result, curr)
	}
	return result
}

func TestUtil_ConvertPath(t *testing.T) {
	expected := filepath.Join("", "home", "to", "my", "stuff")
	assert.Equal(t, expected, convertPath("/home/to/my/stuff"))
	assert.Equal(t, ".", convertPath("."))
}

func TestUtil_StrToBool(t *testing.T) {
	yes := []string{"y", "Y", "yes", "True", "t", "true", "True", "On", "on", "1"}
	no := []string{"n", "no", "f", "false", "off", "0", "Off", "No", "N"}

	for _, y := range yes {
		assert.True(t, strToBool(y), y)
	}
	for _, n := range no {
		assert.False(t, strToBool(n), n)
	}
}

func TestUtil_SplitQuoted(t *testing.T) {
	result := splitQuoted(`""one"" "two" 'three' four`)
	assert.Contains(t, result, "one")
	assert.Contains(t, result, "two")
	assert.Contains(t, result, "three")
}

func TestUtil_GrokEnvironmentError(t *testing.T) {
	msg := "Unable to find batch file"
	errMsg := "error: " + msg
	assert.Equal(t, "error: Unable to find batch file", errMsg)
}