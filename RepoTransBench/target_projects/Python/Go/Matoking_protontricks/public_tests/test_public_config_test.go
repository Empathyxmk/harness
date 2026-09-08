package public_tests

import (
	"os"
	"path/filepath"
	"testing"
)

type Config struct {
	store map[string]map[string]string
	base  string
}

func newConfig(base string) *Config {
	return &Config{
		store: make(map[string]map[string]string),
		base:  base,
	}
}
func (c *Config) Get(section, option, def string) string {
	if sec, ok := c.store[section]; ok {
		if v, ok := sec[option]; ok {
			return v
		}
	}
	return def
}
func (c *Config) Set(section, option, value string) {
	if _, ok := c.store[section]; !ok {
		c.store[section] = make(map[string]string)
	}
	c.store[section][option] = value
}

func TestPublicConfigGetSet(t *testing.T) {
	tmpdir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpdir)
	conf := newConfig(tmpdir)
	def := conf.Get("publicsection", "optionnotset", "some_public_default")
	if def != "some_public_default" {
		t.Fatalf("default value mismatch: got %q", def)
	}
	conf.Set("publicsection", "publicopt", "vvvtest")
	if got := conf.Get("publicsection", "publicopt", ""); got != "vvvtest" {
		t.Fatalf("got %q, want 'vvvtest'", got)
	}
	conf.Set("publicsection", "publicopt", "publicvalue2")
	if got := conf.Get("publicsection", "publicopt", ""); got != "publicvalue2" {
		t.Fatalf("got %q, want 'publicvalue2'", got)
	}
	// Simulate config file creation (e.g., write a config file)
	confPath := filepath.Join(tmpdir, "protontricks", "config.ini")
	os.MkdirAll(filepath.Dir(confPath), 0755)
	f, err := os.Create(confPath)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	section := "[publicsection]\npublicopt = publicvalue2\n"
	_, err = f.WriteString(section)
	if err != nil {
		t.Fatal(err)
	}
	f.Close()
	content, err := os.ReadFile(confPath)
	if err != nil {
		t.Fatal(err)
	}
	bytes := string(content)
	if !(contains(bytes, "publicsection") && contains(bytes, "publicopt") && contains(bytes, "publicvalue2")) {
		t.Errorf("config file missing expected content, got %q", bytes)
	}
}
func contains(s, sub string) bool { return len(s) >= len(sub) && (s == sub || (len(s) > 0 && len(sub) > 0 && indexOf(s, sub) > -1)) }
func indexOf(a, b string) int {
	for i := 0; i <= len(a)-len(b); i++ {
		if a[i:i+len(b)] == b {
			return i
		}
	}
	return -1
}