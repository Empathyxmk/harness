package original

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"precommit_hooks"
)

func TestStringFixerRewrite(t *testing.T) {
	tests := []struct {
		input         string
		output        string
		expectedValue int
	}{
		{"''", "''", 0},
		{"\"\"", "''", 1},
		{"\"'\"", "\"'\"", 0},
		{"\"\\\"\"", "\"\\\"\"", 0},
		{"'\"\"'", "'\"\"'", 0},
		{"x = \"foo\"", "x = 'foo'", 1},
		{"\"'\"", "\"'\"", 0},
		{"\"\"\" Foo \"\"\"", "\"\"\" Foo \"\"\"", 0},
		{"x = \" \\\nfoo \\\n\"\n", "x = ' \\\nfoo \\\n'\n", 1},
		{"\"foo\"\"bar\"", "'foo''bar'", 1},
		{"f'hello{\"world\"}'", "f'hello{\"world\"}'", 0},
	}
	for _, tc := range tests {
		dir, err := ioutil.TempDir("", "strfix")
		assert.NoError(t, err)
		defer os.RemoveAll(dir)
		filepath := filepath.Join(dir, "file.py")
		err = ioutil.WriteFile(filepath, []byte(tc.input), 0644)
		assert.NoError(t, err)
		outval := precommit_hooks.StringFixerMain([]string{filepath})
		bytes, err := ioutil.ReadFile(filepath)
		assert.NoError(t, err)
		assert.Equal(t, tc.output, string(bytes))
		assert.Equal(t, tc.expectedValue, outval)
	}
}

func TestStringFixerRewriteCRLF(t *testing.T) {
	dir, err := ioutil.TempDir("", "strfix_crlf")
	assert.NoError(t, err)
	defer os.RemoveAll(dir)
	path := filepath.Join(dir, "f.py")
	err = ioutil.WriteFile(path, []byte{'"', 'f', 'o', 'o', '"', '\r', '\n', '"', 'b', 'a', 'r', '"', '\r', '\n'}, 0644)
	assert.NoError(t, err)
	ret := precommit_hooks.StringFixerMain([]string{path})
	assert.NotEqual(t, 0, ret)
	content, err := ioutil.ReadFile(path)
	assert.NoError(t, err)
	assert.Equal(t, []byte("'foo'\r\n'bar'\r\n"), content)
}