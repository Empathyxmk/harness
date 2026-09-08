package public_tests

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/jimmc414/onefilellm/utils"
	"github.com/jimmc414/onefilellm/tests/testutil"
)

func TestSafeFileReadUtf8AndFallbackPublic(t *testing.T) {
	tmp := t.TempDir()
	p := filepath.Join(tmp, "foo.txt")
	data := "Testing äßü"
	err := os.WriteFile(p, []byte(data), 0644)
	assert.NoError(t, err)
	assert.Equal(t, data, utils.SafeFileRead(p))

	p2 := filepath.Join(tmp, "bar.txt")
	textLatin1 := []byte{0x6e, 0x69, 0xf1, 0x6f} // "niño"
	err = os.WriteFile(p2, textLatin1, 0644)
	assert.NoError(t, err)
	assert.Equal(t, "niño", utils.SafeFileRead(p2))
}

func TestReadFromClipboardPublic(t *testing.T) {
	origPyperclip := utils.Pyperclip
	defer func() { utils.Pyperclip = origPyperclip }()

	utils.Pyperclip = &testutil.DummyPyperclip{PasteStr: "public clipboard"}
	assert.Equal(t, "public clipboard", utils.ReadFromClipboard())

	utils.Pyperclip = &testutil.DummyPyperclip{PasteStr: "    "}
	assert.Nil(t, utils.ReadFromClipboard())

	utils.Pyperclip = &testutil.DummyPyperclip{PasteErr: true}
	assert.Nil(t, utils.ReadFromClipboard())

	utils.Pyperclip = &testutil.DummyPyperclip{PanicOnce: true}
	assert.Nil(t, utils.ReadFromClipboard())
}

func TestReadFromStdinPublic(t *testing.T) {
	origStdin := os.Stdin
	defer func() { os.Stdin = origStdin }()

	os.Stdin = testutil.NewDummyStdin(true, "")
	assert.Nil(t, utils.ReadFromStdin())

	os.Stdin = testutil.NewDummyStdin(false, "different input\n")
	assert.Equal(t, "different input\n", utils.ReadFromStdin())

	os.Stdin = testutil.NewDummyStdin(false, "")
	assert.Nil(t, utils.ReadFromStdin())

	os.Stdin = testutil.NewErrorStdin(nil)
	assert.Nil(t, utils.ReadFromStdin())
}

func TestDetectTextFormatPublic(t *testing.T) {
	type testpair struct {
		txt      string
		expected string
	}
	formatYaml := "text"
	if utils.HasYaml() {
		formatYaml = "yaml"
	}
	tests := []testpair{
		{`{"foo": 42}`, "json"},
		{`[100, 200, 300]`, "json"},
		{"x: 7\ny: 8", formatYaml},
		{"<HTML>Tag</HTML>", "html"},
		{"<!DOCTYPE HTML>", "html"},
		{"<span>public</span>", "html"},
		{"## Subheader\nSome text", "markdown"},
		{"*item*", "markdown"},
		{"A random sentence", "text"},
		{" ", "text"},
		{"\n\n", "text"},
	}
	for _, tc := range tests {
		assert.Equal(t, tc.expected, utils.DetectTextFormat(tc.txt))
	}
}

func TestParseAsPlaintextAndMarkdownPublic(t *testing.T) {
	s := "xyz"
	assert.Equal(t, s, utils.ParseAsPlaintext(s))
	assert.Equal(t, s, utils.ParseAsMarkdown(s))
}

func TestParseAsJsonAndYamlAndHtmlPublic(t *testing.T) {
	sjson := `{"x": 99, "y": 88}`
	parsed := utils.ParseAsJson(sjson)
	assert.IsType(t, "", parsed)
	if utils.HasYaml() {
		parsedYaml := utils.ParseAsYaml("foo: bar\nbaz: quux")
		assert.IsType(t, "", parsedYaml)
	}
	html := "<html><body>World</body></html>"
	assert.Contains(t, utils.ParseAsHtml(html), "World")
}

func TestDownloadFilePublic(t *testing.T) {
	tmp := t.TempDir()
	dest := filepath.Join(tmp, "some_output.txt")
	resp := &testutil.DummyResp{Content: [][]byte{[]byte("foo"), []byte("bar")}}
	utils.Requests = &testutil.DummyRequests{DownloadResp: resp}
	utils.DownloadFile("https://example.com/some.txt", dest)
	b, err := os.ReadFile(dest)
	assert.NoError(t, err)
	assert.Equal(t, []byte("foobar"), b)
}

func TestIsSameDomainPublic(t *testing.T) {
	assert.True(t, utils.IsSameDomain("https://b.com/page", "https://b.com/y"))
	assert.False(t, utils.IsSameDomain("https://b.com", "https://sub.b.com/a"))
	assert.True(t, utils.IsSameDomain("http://b.com/xy", "https://b.com/zzz"))
}

func TestIsWithinDepthPublic(t *testing.T) {
	assert.True(t, utils.IsWithinDepth("https://b.com", "https://b.com/abc/def", 2))
	assert.False(t, utils.IsWithinDepth("https://b.com", "https://b.com/a/b/c/d", 3))
	assert.False(t, utils.IsWithinDepth("http://b.com", "https://b.com/a/b", 1))
}

func TestIsExcludedFilePublic(t *testing.T) {
	assert.False(t, utils.IsExcludedFile("/bar/src/main.py"))
	assert.True(t, utils.IsExcludedFile("/bar/node_modules/script.js"))
	assert.True(t, utils.IsExcludedFile("/bar/.git/description"))
}

func TestIsAllowedFiletypePublic(t *testing.T) {
	assert.True(t, utils.IsAllowedFiletype("main.go"))
	assert.True(t, utils.IsAllowedFiletype("foo.md"))
	assert.False(t, utils.IsAllowedFiletype("file.dll"))
	assert.True(t, utils.IsAllowedFiletype("file.MD"))
}

func TestEscapeXmlPublic(t *testing.T) {
	raw := "<public>&amp;</public>"
	assert.Equal(t, raw, utils.EscapeXml(raw))
}

func TestParseAsYamlHandlesNoYamlPublic(t *testing.T) {
	orig := utils.YamlEngine
	utils.YamlEngine = nil
	defer func() { utils.YamlEngine = orig }()
	assert.Equal(t, "bar", utils.ParseAsYaml("bar"))
}