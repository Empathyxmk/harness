package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func pyFilesValidator(name string) bool {
	return strings.HasSuffix(name, ".py") && !strings.HasPrefix(name, ".")
}

// simulate executing Koans (would exec external process in Python)
func executeKoansCmd() string {
	return "python3 contemplate_koans.py"
}

func TestPyFilesValidator(t *testing.T) {
	assert.True(t, pyFilesValidator("abc.py"))
	assert.False(t, pyFilesValidator(".abc.py"))
	assert.False(t, pyFilesValidator("abc.txt"))
}

func TestExecuteKoansRuns(t *testing.T) {
	cmd := executeKoansCmd()
	assert.True(t, strings.HasSuffix(cmd, "contemplate_koans.py"))
}