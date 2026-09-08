package public_tests

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/jimmc414/onefilellm/utils"
)

func TestSafeFileReadPublic(t *testing.T) {
	tmpd := t.TempDir()
	utf8Path := filepath.Join(tmpd, "abc.txt")
	err := os.WriteFile(utf8Path, []byte("Public 测试"), 0644)
	assert.NoError(t, err)
	content := utils.SafeFileRead(utf8Path)
	assert.Equal(t, "Public 测试", content)

	latin1Path := filepath.Join(tmpd, "latinpublic.txt")
	buf := []byte{0x6d, 0x61, 0xf1, 0x61, 0x6e, 0x61} // "mañana" in latin-1
	err = os.WriteFile(latin1Path, buf, 0644)
	assert.NoError(t, err)
	content2 := utils.SafeFileRead(latin1Path)
	assert.Equal(t, "mañana", content2)
}

func TestFileExtensionDetectionPublic(t *testing.T) {
	assert.Equal(t, ".js", utils.GetFileExtension("some.JS"))
	assert.Equal(t, ".gz", utils.GetFileExtension("archive.TAR.GZ"))
	assert.Equal(t, "", utils.GetFileExtension("README"))
	assert.Equal(t, ".doc", utils.GetFileExtension("dots.with.many.parts.doc"))
}

func TestIsBinaryFilePublic(t *testing.T) {
	tmpd := t.TempDir()
	tf := filepath.Join(tmpd, "t.txt")
	err := os.WriteFile(tf, []byte("Sample text"), 0644)
	assert.NoError(t, err)
	assert.False(t, utils.IsBinaryFile(tf))
	bf := filepath.Join(tmpd, "b.dat")
	err = os.WriteFile(bf, []byte{0xff, 0xd8, 0xff, 0xdb}, 0644)
	assert.NoError(t, err)
	assert.True(t, utils.IsBinaryFile(bf))
}

func TestIsExcludedFilePublic(t *testing.T) {
	assert.True(t, utils.IsExcludedFile("dist/bundle.js"))
	assert.True(t, utils.IsExcludedFile(".git/hooks/pre-commit"))
	assert.True(t, utils.IsExcludedFile("lib.min.js"))
	assert.True(t, utils.IsExcludedFile("__pycache__/something.pyc"))
	assert.True(t, utils.IsExcludedFile("node_modules/module.js"))
	assert.False(t, utils.IsExcludedFile("main.c"))
	assert.False(t, utils.IsExcludedFile("script.rb"))
}

func TestIsAllowedFiletypePublic(t *testing.T) {
	assert.True(t, utils.IsAllowedFiletype("index.html"))
	assert.True(t, utils.IsAllowedFiletype("data.csv"))
	assert.True(t, utils.IsAllowedFiletype("setup.py"))
	assert.False(t, utils.IsAllowedFiletype("archive.tar.gz"))
	assert.False(t, utils.IsAllowedFiletype("some.dll"))
	assert.False(t, utils.IsAllowedFiletype("compressed.rar"))
}

func TestUrlUtilitiesPublic(t *testing.T) {
	base := "https://public.com/section/"
	assert.True(t, utils.IsSameDomain(base, "https://public.com/else/"))
	assert.False(t, utils.IsSameDomain(base, "https://alt.com/test/"))
	assert.True(t, utils.IsWithinDepth(base, "https://public.com/section/page2", 1))
	assert.True(t, utils.IsWithinDepth(base, "https://public.com/section/inner/page", 2))
	assert.False(t, utils.IsWithinDepth(base, "https://public.com/section/a/b/d", 2))
}

func TestEscapeXmlPublic(t *testing.T) {
	x := "<publicTest>More & stuff</publicTest>"
	assert.Equal(t, x, utils.EscapeXml(x))
}