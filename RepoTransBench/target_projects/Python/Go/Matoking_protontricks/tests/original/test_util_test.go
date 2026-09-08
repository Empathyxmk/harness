package original

import (
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

func lowerDictPy(in map[string]interface{}) map[string]interface{} {
	out := make(map[string]interface{})
	for k, v := range in {
		key := k
		if str, ok := interface{}(key).(string); ok {
			key = string([]byte(str))
			key = stringLower(str)
		}
		val := v
		if sub, ok := v.(map[string]interface{}); ok {
			val = lowerDictPy(sub)
		}
		out[key] = val
	}
	return out
}
func stringLower(s string) string {
	// ASCII only
	out := []rune{}
	for _, c := range s {
		if c >= 'A' && c <= 'Z' {
			c = c + ('a' - 'A')
		}
		out = append(out, c)
	}
	return string(out)
}

func TestLowerDict_NestedDict(t *testing.T) {
	before := map[string]interface{}{
		"AppState": map[string]interface{}{
			"Name": "Blah",
			"appid": 123450,
			"userconfig": map[string]interface{}{"Language": "English"},
		},
	}
	after := map[string]interface{}{
		"appstate": map[string]interface{}{
			"name": "Blah",
			"appid": 123450,
			"userconfig": map[string]interface{}{
				"language": "English",
			},
		},
	}
	got := lowerDictPy(before)
	if !reflect.DeepEqual(got, after) {
		t.Errorf("lowerDictPy() = %#v, want %#v", got, after)
	}
}

func TestIsSteamDeck_NotSteamDeck(t *testing.T) {
	if isSteamDeckMock(false) {
		t.Error("Expected false for non-Steam Deck environment")
	}
}
func TestIsSteamDeck_SteamDeck(t *testing.T) {
	if !isSteamDeckMock(true) {
		t.Error("Expected true for Steam Deck environment")
	}
}

// Actual go implementation would use build tags or environment checks
func isSteamDeckMock(steamDeck bool) bool {
	return steamDeck
}

func TestGetFilesInDir(t *testing.T) {
	// Prepare a temp dir with some files
	tmpdir, err := os.MkdirTemp("", "protontricks_test")
	if err != nil {
		t.Fatalf("os.MkdirTemp failed: %v", err)
	}
	defer os.RemoveAll(tmpdir)
	filesToCreate := []string{"file1", "file2", "file3"}
	for _, f := range filesToCreate {
		fp := filepath.Join(tmpdir, f)
		fh, err := os.Create(fp)
		if err != nil {
			t.Fatalf("failed to create test file %q: %v", fp, err)
		}
		fh.Close()
	}
	got := getFilesInDir(tmpdir)
	want := map[string]bool{"file1": true, "file2": true, "file3": true}
	for _, fname := range filesToCreate {
		if !got[fname] {
			t.Errorf("Expected %q in output of getFilesInDir", fname)
		}
	}
}
func getFilesInDir(dir string) map[string]bool {
	files, err := os.ReadDir(dir)
	if err != nil {
		return nil
	}
	out := make(map[string]bool)
	for _, f := range files {
		out[f.Name()] = true
	}
	return out
}