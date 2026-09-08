package tests

import (
	"os"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestBlacklist_LoadPlainPatterns(t *testing.T) {
	bl := NewBlacklist()

	tmpfile, err := os.CreateTemp("", "blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := ".*forbidden.com.* # info1\n# this is a comment\n.*blockme.net.*\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url1 := NewMultiProtocolURL("http://forbidden.com/page")
	url2 := NewMultiProtocolURL("http://blockme.net/")
	url3 := NewMultiProtocolURL("http://allowed.com/")
	assert.NotNil(t, bl.IsBlacklisted(url1.ToNormalForm(true), url1))
	assert.NotNil(t, bl.IsBlacklisted(url2.ToNormalForm(true), url2))
	assert.Nil(t, bl.IsBlacklisted(url3.ToNormalForm(true), url3))
}

func TestBlacklist_LoadHostPattern(t *testing.T) {
	bl := NewBlacklist()

	tmpfile, err := os.CreateTemp("", "blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := "host example.com # host entry\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url := NewMultiProtocolURL("http://example.com/page")
	assert.NotNil(t, bl.IsBlacklisted(url.ToNormalForm(true), url))
	other := NewMultiProtocolURL("http://test.com/page")
	assert.Nil(t, bl.IsBlacklisted(other.ToNormalForm(true), other))
}

func TestBlacklist_PatternSyntaxError(t *testing.T) {
	bl := NewBlacklist()

	tmpfile, err := os.CreateTemp("", "blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := ".*this[is(bad\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	// Should not throw error
	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)
}

func TestBlacklistInfo_ConstructorWithInvalidPattern(t *testing.T) {
	// Should return error (simulating PatternSyntaxException)
	_, err := NewBlacklistInfo("*This is [invalid", "src", "", "")
	assert.Error(t, err)
}

func TestBlacklist_Caches(t *testing.T) {
	bl := NewBlacklist()

	tmpfile, err := os.CreateTemp("", "blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := ".*foo.com.*\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url := NewMultiProtocolURL("http://foo.com/bar")
	str := url.ToNormalForm(true)
	assert.NotNil(t, bl.IsBlacklisted(str, url))
	// Second time to trigger cache
	assert.NotNil(t, bl.IsBlacklisted(str, url))
}

func TestBlacklist_MissCache(t *testing.T) {
	bl := NewBlacklist()

	tmpfile, err := os.CreateTemp("", "blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := ".*nothingtomatch.net.*\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url := NewMultiProtocolURL("http://notfoo.com/")
	str := url.ToNormalForm(true)
	assert.Nil(t, bl.IsBlacklisted(str, url))
	// Should be cached now
	assert.Nil(t, bl.IsBlacklisted(str, url))
}

func TestBlacklistInfo_Fields(t *testing.T) {
	bi, err := NewBlacklistInfo(".*test.com.*", "src", "information", "host.com")
	assert.NoError(t, err)
	assert.NotNil(t, bi.Pattern)
	assert.Equal(t, "src", bi.Source)
	assert.Equal(t, "information", bi.Info)
	assert.Equal(t, "host.com", bi.Host)
}