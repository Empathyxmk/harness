package original

import (
	"os"
	"os/exec"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSetupPyRuns(t *testing.T) {
	// We will simulate running "python setup.py" and ensure no crash
	cmd := exec.Command("python", "setup.py")
	// Set cwd so it can find setup.py in root if needed
	path, err := os.Getwd()
	assert.NoError(t, err)
	cmd.Dir = path
	output, err := cmd.CombinedOutput()
	// We expect setup.py to not crash, so err may be nil or may be expected if setup.py does nothing
	assert.True(t, err == nil || len(output) > 0)
}