package original

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"
	"time"
	"reflect"
	"strings"

	"github.com/stretchr/testify/assert"
	"github.com/jimmc414/onefilellm/utils"
)

// NOTE: In this Go test file, several comprehensive test functions are translated to match
// the logic of test_all.py in Python. For web, GitHub, Arxiv, and YouTube, 
// you need to mock network and external services as in Python. All the basic logic is included.

func TestSafeFileRead(t *testing.T) {
	tempDir := t.TempDir()
	utf8File := filepath.Join(tempDir, "utf8.txt")
	f1, err := os.Create(utf8File)
	assert.NoError(t, err)
	_, err = f1.WriteString("Hello 世界")
	assert.NoError(t, err)
	f1.Close()
	content := utils.SafeFileRead(utf8File)
	assert.Equal(t, "Hello 世界", content)

	latin1File := filepath.Join(tempDir, "latin1.txt")
	file, err := os.Create(latin1File)
	assert.NoError(t, err)
	file.Write([]byte{0x43, 0x61, 0x66, 0xe9}) // Café in latin-1
	file.Close()
	content2 := utils.SafeFileRead(latin1File)
	assert.Equal(t, "Café", content2)
}

func TestFileExtensionDetection(t *testing.T) {
	assert.Equal(t, ".py", utils.GetFileExtension("test.py"))
	assert.Equal(t, ".py", utils.GetFileExtension("TEST.PY"))
	assert.Equal(t, "", utils.GetFileExtension("no_extension"))
	assert.Equal(t, ".txt", utils.GetFileExtension("multiple.dots.txt"))
}

func TestIsBinaryFile(t *testing.T) {
	tempDir := t.TempDir()
	textFile := filepath.Join(tempDir, "text.txt")
	os.WriteFile(textFile, []byte("This is text"), 0644)
	assert.False(t, utils.IsBinaryFile(textFile))
	binaryFile := filepath.Join(tempDir, "binary.bin")
	os.WriteFile(binaryFile, []byte{0x00, 0x01, 0x02, 0x03}, 0644)
	assert.True(t, utils.IsBinaryFile(binaryFile))
}

func TestIsExcludedFile(t *testing.T) {
	assert.True(t, utils.IsExcludedFile("test.pb.go"))
	assert.True(t, utils.IsExcludedFile("file_test.go"))
	assert.True(t, utils.IsExcludedFile("script.min.js"))
	assert.True(t, utils.IsExcludedFile("__pycache__/file.pyc"))
	assert.True(t, utils.IsExcludedFile("node_modules/package.json"))
	assert.False(t, utils.IsExcludedFile("main.go"))
	assert.False(t, utils.IsExcludedFile("app.js"))
}

func TestIsAllowedFileType(t *testing.T) {
	assert.True(t, utils.IsAllowedFiletype("script.py"))
	assert.True(t, utils.IsAllowedFiletype("README.md"))
	assert.True(t, utils.IsAllowedFiletype("config.yaml"))
	assert.False(t, utils.IsAllowedFiletype("image.png"))
	assert.False(t, utils.IsAllowedFiletype("binary.exe"))
	assert.False(t, utils.IsAllowedFiletype("archive.zip"))
}

func TestUrlUtilities(t *testing.T) {
	base := "https://example.com/docs/"
	assert.True(t, utils.IsSameDomain(base, "https://example.com/other/"))
	assert.False(t, utils.IsSameDomain(base, "https://other.com/docs/"))
	assert.True(t, utils.IsWithinDepth(base, "https://example.com/docs/page1", 1))
	assert.True(t, utils.IsWithinDepth(base, "https://example.com/docs/sub/page", 2))
	assert.False(t, utils.IsWithinDepth(base, "https://example.com/docs/a/b/c", 2))
}

func TestEscapeXml(t *testing.T) {
	text := "<tag>Content & more</tag>"
	assert.Equal(t, text, utils.EscapeXml(text))
}

func TestFormatDetection(t *testing.T) {
	assert.Equal(t, "text", utils.DetectTextFormat("Just plain text"))
	assert.Equal(t, "text", utils.DetectTextFormat(""))
	assert.Equal(t, "json", utils.DetectTextFormat(`{"key": "value"}`))
	assert.Equal(t, "json", utils.DetectTextFormat("[1, 2, 3]"))
	assert.Equal(t, "json", utils.DetectTextFormat("{\n  \"nested\": {\n    \"data\": true\n  }\n}"))
	assert.Equal(t, "html", utils.DetectTextFormat("<!DOCTYPE html><html></html>"))
	assert.Equal(t, "html", utils.DetectTextFormat("<html><body>Content</body></html>"))
	assert.Equal(t, "html", utils.DetectTextFormat("<div>Single tag</div>"))
	assert.Equal(t, "markdown", utils.DetectTextFormat("# Heading\n\nParagraph"))
	assert.Equal(t, "markdown", utils.DetectTextFormat("**Bold** and *italic*"))
	assert.Equal(t, "markdown", utils.DetectTextFormat("- List item\n- Another item"))
	assert.Equal(t, "markdown", utils.DetectTextFormat("[Link](https://example.com)"))
	assert.Equal(t, "markdown", utils.DetectTextFormat("