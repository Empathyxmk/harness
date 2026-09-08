package original

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"precommit_hooks"
)

func TestCheckFileBasicTypes(t *testing.T) {
	code := `
a = list()
b = dict()
c = float()
d = int()
e = complex()
f = str()
g = tuple()
`
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "basic_types.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	res := precommit_hooks.CheckBuiltinLiteralsCheckFile(filePath, nil, true)
	typesReported := make(map[string]struct{})
	for _, c := range res {
		typesReported[c.Name] = struct{}{}
	}
	want := map[string]struct{}{"list": {}, "dict": {}, "float": {}, "int": {}, "complex": {}, "str": {}, "tuple": {}}
	assert.Equal(t, want, typesReported)
}

func TestCheckFileWithIgnore(t *testing.T) {
	code := `
a = list()
b = dict()
c = int()
`
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "ignore_types.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	ignore := []string{"dict", "list"}
	res := precommit_hooks.CheckBuiltinLiteralsCheckFile(filePath, ignore, true)
	typesReported := make(map[string]struct{})
	for _, c := range res {
		typesReported[c.Name] = struct{}{}
	}
	assert.Contains(t, typesReported, "int")
	_, listOk := typesReported["list"]
	assert.False(t, listOk)
	_, dictOk := typesReported["dict"]
	assert.False(t, dictOk)
}

func TestCheckFileDictWithKwargs(t *testing.T) {
	code := `
a = dict(foo=1)
`
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "dict_kwargs.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	// default (allow_dict_kwargs=True), should be ignored
	res := precommit_hooks.CheckBuiltinLiteralsCheckFile(filePath, nil, true)
	assert.Equal(t, []precommit_hooks.ConstructorCall{}, res)
	// allow_dict_kwargs=False, should NOT ignore, should be found
	res2 := precommit_hooks.CheckBuiltinLiteralsCheckFile(filePath, nil, false)
	assert.True(t, len(res2) > 0 && res2[0].Name == "dict")
}

func TestCheckFileAttributeCalls(t *testing.T) {
	code := `
import builtins
a = builtins.list()
`
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "attributes.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	res := precommit_hooks.CheckBuiltinLiteralsCheckFile(filePath, nil, true)
	assert.Equal(t, []precommit_hooks.ConstructorCall{}, res)
}

func TestMainPrints(t *testing.T) {
	code := "a = list()\n"
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "main1.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	rc, out := runCheckBuiltinLiteralsMainCapture([]string{filePath})
	assert.NotEqual(t, 0, rc)
	assert.Contains(t, out, "replace list()")
}

func TestMainIgnore(t *testing.T) {
	code := "a = list()\n"
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "main2.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	rc := precommit_hooks.CheckBuiltinLiteralsMain([]string{filePath, "--ignore", "list"})
	assert.Equal(t, 0, rc)
}

func TestMainAllowNoAllowDictKwargs(t *testing.T) {
	code := "a = dict(foo=1)\n"
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "main3.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	rc, out := runCheckBuiltinLiteralsMainCapture([]string{filePath, "--no-allow-dict-kwargs"})
	assert.NotEqual(t, 0, rc)
	assert.Contains(t, out, "replace dict()")
}

func TestParseIgnore(t *testing.T) {
	res := precommit_hooks.CheckBuiltinLiteralsParseIgnore("float,str")
	want := map[string]struct{}{"float": {}, "str": {}}
	assert.Equal(t, want, res)
}

func TestMainNoCalls(t *testing.T) {
	code := "a = 1\nb = 2\n"
	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "nothing.py")
	err := os.WriteFile(filePath, []byte(code), 0644)
	assert.NoError(t, err)
	rc, out := runCheckBuiltinLiteralsMainCapture([]string{filePath})
	assert.NotContains(t, out, "replace")
	assert.Equal(t, 0, rc)
}

// Helper for capturing output during main run
func runCheckBuiltinLiteralsMainCapture(args []string) (int, string) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	rc := precommit_hooks.CheckBuiltinLiteralsMain(args)
	w.Close()
	out, _ := ioutil.ReadAll(r)
	os.Stdout = old
	return rc, string(out)
}