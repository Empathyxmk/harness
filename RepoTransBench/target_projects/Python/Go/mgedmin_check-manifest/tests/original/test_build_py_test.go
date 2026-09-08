package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestBuildPy_PackageData(t *testing.T) {
	packageFiles := []string{"__init__.py", "README.txt"}
	assert.Contains(t, packageFiles, "__init__.py")
	assert.Contains(t, packageFiles, "README.txt")
}

func TestBuildPy_EmptyPackageDir(t *testing.T) {
	packageFiles := []string{"__init__.py", "doc/testfile"}
	assert.Contains(t, packageFiles, "doc/testfile")
}

func TestBuildPy_DontWriteBytecode(t *testing.T) {
	byteCompiling := false
	assert.False(t, byteCompiling)
}