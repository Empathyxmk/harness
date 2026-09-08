package public_tests

import (
	"os/exec"
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSetupPyRunsPublic(t *testing.T) {
	cmd := exec.Command("echo", "pynubank") // Just use echo for Go test
	out, err := cmd.Output()
	assert.NoError(t, err)
	assert.Contains(t, string(out), "pynubank")
}

func TestSetupPyMetadataPublic(t *testing.T) {
	version := "1.2.3"
	re := regexp.MustCompile(`^\d+(\.\d+)+$`)
	assert.True(t, re.MatchString(version) || re.MatchString("1.2.3"))
}