package original

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"precommit_hooks"
)

var (
	GITHUB_URL          = []byte("https://github.com/foo/bar/blob/master/file.py#L2")
	GITHUB_URL_BRANCH   = []byte("https://github.com/foo/bar/blob/feature/file.py#L20")
	GITHUB_URL_WITH_HASH = []byte("https://github.com/foo/bar/blob/09dcbc08/file.py#L1")
	NONMATCH            = []byte("https://notgithub.com/foo/bar/blob/master/file.py#L1")
)

func TestGetPatternMatchesExpected(t *testing.T) {
	pattern := precommit_hooks.CheckVcsPermalinksGetPattern("github.com")
	assert.True(t, pattern.Match(GITHUB_URL_BRANCH))
	assert.False(t, pattern.Match(GITHUB_URL_WITH_HASH))
	assert.True(t, pattern.Match(GITHUB_URL))
}

func TestCheckFilenameDetects(t *testing.T) {
	dir := t.TempDir()
	thefile := filepath.Join(dir, "testfile.txt")
	lines := [][]byte{
		[]byte("some stuff\n"),
		append(GITHUB_URL, []byte("\n")...),
		append(NONMATCH, []byte("\n")...),
	}
	// Join bytes
	content := bytes.Join(lines, []byte{})
	err := os.WriteFile(thefile, content, 0644)
	assert.NoError(t, err)
	patterns := []*precommit_hooks.VcsPermalinkPattern{precommit_hooks.CheckVcsPermalinksGetPattern("github.com")}
	buf := &bytes.Buffer{}
	outFn := func(a ...any) (int, error) {
		return buf.WriteString(a[0].(string))
	}
	ret := precommit_hooks.CheckVcsPermalinksCheckFilename(thefile, patterns, outFn)
	assert.Equal(t, 1, ret)
	assert.Contains(t, buf.String(), thefile)
}

func TestCheckFilenameNoHits(t *testing.T) {
	dir := t.TempDir()
	thefile := filepath.Join(dir, "testfile2.txt")
	content := append([]byte("Something else\n"), NONMATCH...)
	content = append(content, '\n')
	err := os.WriteFile(thefile, content, 0644)
	assert.NoError(t, err)
	patterns := []*precommit_hooks.VcsPermalinkPattern{precommit_hooks.CheckVcsPermalinksGetPattern("github.com")}
	buf := &bytes.Buffer{}
	outFn := func(a ...any) (int, error) {
		return buf.WriteString(a[0].(string))
	}
	ret := precommit_hooks.CheckVcsPermalinksCheckFilename(thefile, patterns, outFn)
	assert.Equal(t, 0, ret)
	assert.NotContains(t, buf.String(), "Non-permanent")
}

func TestMainPrintsWarning(t *testing.T) {
	dir := t.TempDir()
	thefile := filepath.Join(dir, "foo.txt")
	content := append(GITHUB_URL, []byte("\n")...)
	err := os.WriteFile(thefile, content, 0644)
	assert.NoError(t, err)

	buf := &bytes.Buffer{}
	oldOut := precommit_hooks.Stdout
	precommit_hooks.Stdout = buf
	defer func() { precommit_hooks.Stdout = oldOut }()

	defer func() {
		r := recover()
		assert.NotNil(t, r)
		assert.Contains(t, buf.String(), "Non-permanent github link detected")
	}()

	precommit_hooks.CheckVcsPermalinksMain([]string{thefile})
}

func TestMainNoWarn(t *testing.T) {
	dir := t.TempDir()
	thefile := filepath.Join(dir, "foo2.txt")
	content := append(NONMATCH, []byte("\n")...)
	err := os.WriteFile(thefile, content, 0644)
	assert.NoError(t, err)
	buf := &bytes.Buffer{}
	oldOut := precommit_hooks.Stdout
	precommit_hooks.Stdout = buf
	defer func() { precommit_hooks.Stdout = oldOut }()
	ret := precommit_hooks.CheckVcsPermalinksMain([]string{thefile})
	assert.NotContains(t, buf.String(), "Non-permanent")
	assert.Equal(t, 0, ret)
}

func TestMainAdditionalGithubDomain(t *testing.T) {
	dir := t.TempDir()
	thefile := filepath.Join(dir, "foo3.txt")
	domain := "gh.acme.com"
	url := []byte("https://" + domain + "/u/b/blob/main/f.py#L99")
	content := append(url, []byte("\n")...)
	err := os.WriteFile(thefile, content, 0644)
	assert.NoError(t, err)
	buf := &bytes.Buffer{}
	oldOut := precommit_hooks.Stdout
	precommit_hooks.Stdout = buf
	defer func() { precommit_hooks.Stdout = oldOut }()

	defer func() {
		r := recover()
		assert.NotNil(t, r)
		assert.Contains(t, buf.String(), "Non-permanent")
	}()
	precommit_hooks.CheckVcsPermalinksMain([]string{thefile, "--additional-github-domain", domain})

}