package original

import (
	"testing"
	"regexp"

	"github.com/stretchr/testify/assert"
)

func Uppercase(s string) string {
	return strings.ToUpper(s)
}

func ValidEmail(email string) bool {
	re := regexp.MustCompile(`^[^@]+@[^@]+\.[^@]+$`)
	return re.MatchString(email)
}

func TestUppercase(t *testing.T) {
	assert.Equal(t, "HELLO", Uppercase("hello"))
	assert.Equal(t, "A", Uppercase("A"))
}

func TestValidEmail(t *testing.T) {
	assert.True(t, ValidEmail("abc@example.com"))
	assert.False(t, ValidEmail("not an email"))
	assert.False(t, ValidEmail("foo@bar"))
	assert.False(t, ValidEmail("foo@bar."))
}