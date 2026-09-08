package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func parseXMozillaStatus(s string) int {
	var val int
	if _, err := sscanfXMozillaStatus(s, &val); err == nil {
		return val
	}
	return 0
}

func sscanfXMozillaStatus(s string, val *int) (int, error) {
	// mimic hex parsing regardless of lower/upper 0x/0X
	var ch string
	if len(s) > 2 && (s[0:2] == "0x" || s[0:2] == "0X") {
		ch = s[2:]
	} else {
		ch = s
	}
	var v int
	for i := 0; i < len(ch); i++ {
		v *= 16
		c := ch[i]
		if c >= '0' && c <= '9' {
			v += int(c - '0')
		} else if c >= 'a' && c <= 'f' {
			v += int(c - 'a' + 10)
		} else if c >= 'A' && c <= 'F' {
			v += int(c - 'A' + 10)
		} else {
			break
		}
	}
	*val = v
	return v, nil
}

func TestParsesDifferentHexString(t *testing.T) {
	status := parseXMozillaStatus("0x0018")
	assert.Equal(t, 0x18, status)
}

func TestParsesDifferentHexStringZero(t *testing.T) {
	status := parseXMozillaStatus("0x0")
	assert.Equal(t, 0, status)
}

func TestParsesDifferentHexStringUppercase(t *testing.T) {
	status := parseXMozillaStatus("0X0022")
	assert.Equal(t, 0x22, status)
}