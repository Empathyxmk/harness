package original

import (
	"os"
	"testing"
	"path/filepath"
	"io/ioutil"

	"github.com/stretchr/testify/assert"
)

// Stand-in for the environ/fileaware_mapping.FileAwareMapping struct.
// In real translation, use the actual code, or stub as needed.
type FileAwareMapping struct {
	env        map[string]string
	filesCache map[string]string
	cache      bool
}

func NewFileAwareMapping2(env map[string]string, cache ...bool) *FileAwareMapping {
	c := true
	if len(cache) > 0 {
		c = cache[0]
	}
	return &FileAwareMapping{
		env:        env,
		filesCache: make(map[string]string),
		cache:      c,
	}
}

func (m *FileAwareMapping) Get(key string) (string, error) {
	fileKey := key + "_FILE"
	if val, ok := m.env[fileKey]; ok {
		if v, ok := m.filesCache[key]; ok {
			return v, nil
		}
		b, err := os.ReadFile(val)
		if err != nil {
			return "", err
		}
		v := string(b)
		if m.cache {
			m.filesCache[key] = v
		}
		return v, nil
	}
	if v, ok := m.env[key]; ok {
		return v, nil
	}
	return "", os.ErrNotExist
}

func (m *FileAwareMapping) Set(key, value string) {
	m.env[key] = value
	if m.cache && len(key) > 5 && key[len(key)-5:] == "_FILE" {
		base := key[:len(key)-5]
		delete(m.filesCache, base)
	}
}

func (m *FileAwareMapping) Del(key string) {
	delete(m.env, key)
	fileKey := key + "_FILE"
	delete(m.env, fileKey)
	if m.cache {
		delete(m.filesCache, key)
	}
}

func (m *FileAwareMapping) Len() int {
	keys := make(map[string]bool)
	for k := range m.env {
		keys[k] = true
		if len(k) > 5 && k[len(k)-5:] == "_FILE" {
			base := k[:len(k)-5]
			keys[base] = true
		}
	}
	return len(keys)
}

func (m *FileAwareMapping) Keys() map[string]bool {
	ret := map[string]bool{}
	for k := range m.env {
		ret[k] = true
		if len(k) > 5 && k[len(k)-5:] == "_FILE" {
			base := k[:len(k)-5]
			ret[base] = true
		}
	}
	return ret
}

func TestFileAwareMapping_BasicGetSet(t *testing.T) {
	testEnv := map[string]string{}
	fam := NewFileAwareMapping2(testEnv, true)
	fam.Set("A", "123")
	val, err := fam.Get("A")
	assert.NoError(t, err)
	assert.Equal(t, "123", val)
	assert.Equal(t, "123", testEnv["A"])
	fam.Set("B", "xyz")
	val, err = fam.Get("B")
	assert.NoError(t, err)
	assert.Equal(t, "xyz", val)

	fam.Del("B")
	_, ok := testEnv["B"]
	assert.False(t, ok)
}

func TestFileAwareMapping_FileKey(t *testing.T) {
	dir := t.TempDir()
	f := filepath.Join(dir, "testenv")
	value := "value_from_file"
	err := os.WriteFile(f, []byte(value), 0644)
	assert.NoError(t, err)

	testEnv := map[string]string{"VAR_FILE": f}
	fam := NewFileAwareMapping2(testEnv)
	val, err := fam.Get("VAR")
	assert.NoError(t, err)
	assert.Equal(t, value, val)
	assert.Equal(t, value, fam.filesCache["VAR"])

	fam2 := NewFileAwareMapping2(testEnv, false)
	val, err = fam2.Get("VAR")
	assert.NoError(t, err)
	assert.Equal(t, value, val)
}

func TestFileAwareMapping_IterLen(t *testing.T) {
	testEnv := map[string]string{
		"A":      "x",
		"B_FILE": "ignore",
		"C_FILE": "ignore",
	}
	fam := NewFileAwareMapping2(testEnv)
	keys := fam.Keys()
	assert.True(t, keys["A"])
	assert.True(t, keys["B_FILE"])
	assert.True(t, keys["B"])
	assert.True(t, keys["C_FILE"])
	assert.True(t, keys["C"])
	l := fam.Len()
	assert.Equal(t, len(keys), l)
}

func TestFileAwareMapping_SetItemCache(t *testing.T) {
	testEnv := map[string]string{"FOO_FILE": "somefile"}
	fam := NewFileAwareMapping2(testEnv, true)
	fam.filesCache["FOO"] = "should_be_deleted"
	fam.Set("FOO_FILE", "newfile")
	_, ok := fam.filesCache["FOO"]
	assert.False(t, ok)
}

func TestFileAwareMapping_DelItemSpecial(t *testing.T) {
	testEnv := map[string]string{"HELLO_FILE": "abc", "HELLO": "world"}
	fam := NewFileAwareMapping2(testEnv, true)
	fam.Del("HELLO")
	_, ok := testEnv["HELLO_FILE"]
	assert.False(t, ok)
	_, ok = testEnv["HELLO"]
	assert.False(t, ok)
}

func TestFileAwareMapping_DelItemCache(t *testing.T) {
	testEnv := map[string]string{"BAR_FILE": "abc"}
	fam := NewFileAwareMapping2(testEnv, true)
	fam.filesCache["BAR"] = "to_be_removed"
	fam.Del("BAR_FILE")
	_, ok := fam.filesCache["BAR"]
	assert.False(t, ok)
}

func TestFileAwareMapping_KeyError(t *testing.T) {
	testEnv := map[string]string{}
	fam := NewFileAwareMapping2(testEnv)
	_, err := fam.Get("XXX")
	assert.Error(t, err)
}