package original

import (
	"bytes"
	"errors"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/jimmc414/onefilellm/tests/testutil"
	"github.com/jimmc414/onefilellm/utils"
)

// DummyPyperclip implements minimal clipboard interface for tests
type DummyPyperclip struct {
	PasteFunc func() (string, error)
}

func (d *DummyPyperclip) Paste() (string, error) {
	return d.PasteFunc()
}

func TestSafeFileReadUtf8AndFallback(t *testing.T) {
	tmpdir := t.TempDir()
	file1 := filepath.Join(tmpdir, "f.txt")
	data := "Hello äöü"
	err := os.WriteFile(file1, []byte(data), 0644)
	assert.NoError(t, err)
	content := utils.SafeFileRead(file1)
	assert.Equal(t, data, content)

	// Write a latin1 file
	file2 := filepath.Join(tmpdir, "f2.txt")
	textLatin1 := []byte{0x63, 0x61, 0x66, 0xe9} // "café" latin1
	err = os.WriteFile(file2, textLatin1, 0644)
	assert.NoError(t, err)
	content2 := utils.SafeFileRead(file2)
	assert.Equal(t, "café", content2)
}

func TestReadFromClipboard(t *testing.T) {
	origPyperclip := utils.Pyperclip
	defer func() { utils.Pyperclip = origPyperclip }()

	// Case 1: clipboard with text
	utils.Pyperclip = &DummyPyperclip{
		PasteFunc: func() (string, error) {
			return "clipboard content", nil
		},
	}
	assert.Equal(t, "clipboard content", utils.ReadFromClipboard())
	// Case 2: clipboard empty string
	utils.Pyperclip = &DummyPyperclip{
		PasteFunc: func() (string, error) {
			return "   ", nil
		},
	}
	assert.Nil(t, utils.ReadFromClipboard())
	// Case 3: exception occurs
	utils.Pyperclip = &DummyPyperclip{
		PasteFunc: func() (string, error) {
			return "", errors.New("err")
		},
	}
	assert.Nil(t, utils.ReadFromClipboard())
	// Generic Exception
	utils.Pyperclip = &DummyPyperclip{
		PasteFunc: func() (string, error) {
			return "", errors.New("x")
		},
	}
	assert.Nil(t, utils.ReadFromClipboard())
}

func TestReadFromStdin(t *testing.T) {
	origStdin := os.Stdin
	defer func() { os.Stdin = origStdin }()

	// Case 1: stdin isatty = true
	os.Stdin = testutil.NewDummyStdin(true, "")
	assert.Nil(t, utils.ReadFromStdin())

	// Case 2: stdin isatty = false, stdin has content
	os.Stdin = testutil.NewDummyStdin(false, "something\n")
	assert.Equal(t, "something\n", utils.ReadFromStdin())

	// Case 3: stdin isatty = false, stdin empty
	os.Stdin = testutil.NewDummyStdin(false, "")
	assert.Nil(t, utils.ReadFromStdin())

	// Case 4: stdin error
	os.Stdin = testutil.NewErrorStdin(errors.New("fail"))
	assert.Nil(t, utils.ReadFromStdin())
}

func TestDetectTextFormat(t *testing.T) {
	tests := []struct {
		txt      string
		expected string
	}{
		{`{"a": 1}`, "json"},
		{`[1, 2, 3]`, "json"},
		{"a: 3\nb: 4", func() string {
			if utils.HasYaml() {
				return "yaml"
			}
			return "text"
		}()},
		{"<html>Tag</html>", "html"},
		{"<!DOCTYPE html>", "html"},
		{"<div>hello</div>", "html"},
		{"# Header\nSome text", "markdown"},
		{"**bold**", "markdown"},
		{"Just some text", "text"},
		{"", "text"},
		{" \n\r ", "text"},
	}
	for _, tc := range tests {
		assert.Equal(t, tc.expected, utils.DetectTextFormat(tc.txt))
	}
}

func TestParseAsPlaintextAndMarkdown(t *testing.T) {
	s := "abc"
	assert.Equal(t, s, utils.ParseAsPlaintext(s))
	assert.Equal(t, s, utils.ParseAsMarkdown(s))
}

func TestParseAsJsonAndYamlAndHtml(t *testing.T) {
	sjson := `{"a": 1, "b": 2}`
	parsed := utils.ParseAsJson(sjson)
	assert.IsType(t, "", parsed)
	// YAML (if present)
	if utils.HasYaml() {
		parsedYaml := utils.ParseAsYaml("k: v\nb: 3")
		assert.IsType(t, "", parsedYaml)
	}
	html := "<html><body>Hello</body></html>"
	assert.Contains(t, utils.ParseAsHtml(html), "Hello")
}

func TestDownloadFile(t *testing.T) {
	url := "https://example.com/test.txt"
	tmpdir := t.TempDir()
	dest := filepath.Join(tmpdir, "out.txt")
	resp := &testutil.DummyResp{
		Content: [][]byte{[]byte("hello"), []byte("world")},
	}
	utils.Requests = &testutil.DummyRequests{DownloadResp: resp}
	utils.DownloadFile(url, dest)
	// The file should exist
	data, err := os.ReadFile(dest)
	assert.NoError(t, err)
	assert.Equal(t, []byte("helloworld"), data)
}

func TestIsSameDomain(t *testing.T) {
	assert.True(t, utils.IsSameDomain("https://a.com/page", "https://a.com/x"))
	assert.False(t, utils.IsSameDomain("https://a.com", "https://sub.a.com/x"))
	assert.True(t, utils.IsSameDomain("http://a.com/x", "https://a.com/other"))
}

func TestIsWithinDepth(t *testing.T) {
	assert.True(t, utils.IsWithinDepth("https://a.com", "https://a.com/foo/bar", 2))
	assert.False(t, utils.IsWithinDepth("https://a.com", "https://a.com/foo/bar/yep", 2))
	assert.False(t, utils.IsWithinDepth("http://a.com", "https://a.com/f/2", 1))
}

func TestIsExcludedFile(t *testing.T) {
	assert.False(t, utils.IsExcludedFile("/foo/bar/readme.md"))
	assert.True(t, utils.IsExcludedFile("/foo/dist/file.txt"))
	assert.True(t, utils.IsExcludedFile("/foo/.git/config"))
}

func TestIsAllowedFiletype(t *testing.T) {
	assert.True(t, utils.IsAllowedFiletype("file.py"))
	assert.True(t, utils.IsAllowedFiletype("file.txt"))
	assert.False(t, utils.IsAllowedFiletype("file.exe"))
	assert.True(t, utils.IsAllowedFiletype("file.PY"))
}

func TestEscapeXml(t *testing.T) {
	raw := "<a>&b</a>"
	assert.Equal(t, raw, utils.EscapeXml(raw))
}

func TestParseAsYamlHandlesNoYaml(t *testing.T) {
	orig := utils.YamlEngine
	utils.YamlEngine = nil
	defer func() { utils.YamlEngine = orig }()
	assert.Equal(t, "foo", utils.ParseAsYaml("foo"))
}