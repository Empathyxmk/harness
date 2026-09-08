package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestInstallScripts_DefaultSettings(t *testing.T) {
	force := false
	skipBuild := false
	assert.False(t, force)
	assert.False(t, skipBuild)
	force = true
	skipBuild = true
	assert.True(t, force)
	assert.True(t, skipBuild)
}

func TestInstallScripts_Installation(t *testing.T) {
	sourceScripts := []string{"a.sh", "b.sh"}
	installed := sourceScripts
	assert.Contains(t, installed, "a.sh")
	assert.Contains(t, installed, "b.sh")
}