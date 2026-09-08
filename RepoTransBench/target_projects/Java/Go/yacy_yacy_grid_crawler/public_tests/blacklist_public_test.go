package public_tests

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"yacy_grid_crawler/tests"
)

func TestBlacklistPublic_LoadPlainPatterns_Public(t *testing.T) {
	bl := tests.NewBlacklist()
	tmpfile, err := os.CreateTemp("", "public_blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := ".*denythis.org.* # info2\n# another comment\n.*lockme.io.*\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url1 := tests.NewMultiProtocolURL("http://denythis.org/document")
	url2 := tests.NewMultiProtocolURL("http://lockme.io/data")
	url3 := tests.NewMultiProtocolURL("http://good.com/")
	assert.NotNil(t, bl.IsBlacklisted(url1.ToNormalForm(true), url1))
	assert.NotNil(t, bl.IsBlacklisted(url2.ToNormalForm(true), url2))
	assert.Nil(t, bl.IsBlacklisted(url3.ToNormalForm(true), url3))
}

func TestBlacklistPublic_LoadHostPattern_Public(t *testing.T) {
	bl := tests.NewBlacklist()
	tmpfile, err := os.CreateTemp("", "public_blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := "host othersite.org # public host entry\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url := tests.NewMultiProtocolURL("http://othersite.org/info")
	assert.NotNil(t, bl.IsBlacklisted(url.ToNormalForm(true), url))
	other := tests.NewMultiProtocolURL("http://diffsite.org/home")
	assert.Nil(t, bl.IsBlacklisted(other.ToNormalForm(true), other))
}

func TestBlacklistPublic_PatternSyntaxError_Public(t *testing.T) {
	bl := tests.NewBlacklist()
	tmpfile, err := os.CreateTemp("", "public_blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	content := ".*wrong(syntax\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	// Should not throw error
	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)
}

func TestBlacklistPublic_BlacklistInfoConstructorWithInvalidPattern_Public(t *testing.T) {
	_, err := tests.NewBlacklistInfo("*Wrong [pattern", "src2", "", "")
	assert.Error(t, err)
}

func TestBlacklistPublic_Caches_Public(t *testing.T) {
	bl := tests.NewBlacklist()
	tmpfile, err := os.CreateTemp("", "public_blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()
	content := ".*bar.org.*\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url := tests.NewMultiProtocolURL("http://bar.org/example")
	str := url.ToNormalForm(true)
	assert.NotNil(t, bl.IsBlacklisted(str, url))
	assert.NotNil(t, bl.IsBlacklisted(str, url))
}

func TestBlacklistPublic_MissCache_Public(t *testing.T) {
	bl := tests.NewBlacklist()
	tmpfile, err := os.CreateTemp("", "public_blacklist-*.txt")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()
	content := ".*abcxyz42.com.*\n"
	_, err = tmpfile.WriteString(content)
	assert.NoError(t, err)
	tmpfile.Sync()

	err = bl.Load(tmpfile.Name())
	assert.NoError(t, err)

	url := tests.NewMultiProtocolURL("http://notbar.org/home")
	str := url.ToNormalForm(true)
	assert.Nil(t, bl.IsBlacklisted(str, url))
	assert.Nil(t, bl.IsBlacklisted(str, url))
}

func TestBlacklistPublic_BlacklistInfoFields_Public(t *testing.T) {
	bi, err := tests.NewBlacklistInfo(".*another-test.org.*", "srcFile", "extra-info", "host.org")
	assert.NoError(t, err)
	assert.NotNil(t, bi.Pattern)
	assert.Equal(t, "srcFile", bi.Source)
	assert.Equal(t, "extra-info", bi.Info)
	assert.Equal(t, "host.org", bi.Host)
}