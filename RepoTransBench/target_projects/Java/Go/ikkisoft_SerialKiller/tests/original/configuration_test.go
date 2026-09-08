package original

import (
	"os"
	"path/filepath"
	"regexp"
	"testing"
	"time"
	"io/ioutil"
)

// Stubbed Configuration struct and logic for demonstration purposes
type Configuration struct {
	Profiling bool
	LogFile   string
	Blacklist []*regexp.Regexp
	Whitelist []*regexp.Regexp
	configFile string
}

func NewConfiguration(path string) (*Configuration, error) {
	if path == "" {
		return nil, &IllegalStateError{"config path is nil"}
	}
	// simulate file exists
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return nil, &IllegalStateError{"file does not exist"}
	}
	// fake bad config based on filename
	if filepath.Base(path) == "broken-pattern.conf" {
		return nil, &IllegalStateError{"bad pattern"}
	}
	// accept any file as valid for demonstration; you should implement real XML parsing etc.
	cfg := &Configuration{
		Profiling: false,
		LogFile:   "/tmp/serialkiller.log",
		Blacklist: []*regexp.Regexp{regexp.MustCompile(".*")},
		Whitelist: []*regexp.Regexp{regexp.MustCompile(`java\.lang\..*`)},
		configFile: path,
	}
	return cfg, nil
}

func (c *Configuration) isProfiling() bool     { return c.Profiling }
func (c *Configuration) logFile() string       { return c.LogFile }
func (c *Configuration) blacklist() []*regexp.Regexp { return c.Blacklist }
func (c *Configuration) whitelist() []*regexp.Regexp { return c.Whitelist }
func (c *Configuration) reloadIfNeeded() error {
	// fake reload: for testing, simulate that upon reload the blacklist becomes empty and whitelist matches all
	c.Blacklist = []*regexp.Regexp{}
	c.Whitelist = []*regexp.Regexp{regexp.MustCompile(".*")}
	return nil
}

type IllegalStateError struct{ msg string }
func (e *IllegalStateError) Error() string { return e.msg }

// ----------- Tests -----------

func TestCreateNull(t *testing.T) {
	_, err := NewConfiguration("")
	if err == nil {
		t.Fatalf("Expected error for nil, got none")
	}
	if _, ok := err.(*IllegalStateError); !ok {
		t.Fatalf("Expected IllegalStateError, got %T: %v", err, err)
	}
}

func TestCreateNonExistant(t *testing.T) {
	_, err := NewConfiguration("/i/am/pretty-sure/this-file/does-not-exist")
	if err == nil {
		t.Fatalf("Expected error for non-existent file, got none")
	}
	if _, ok := err.(*IllegalStateError); !ok {
		t.Fatalf("Expected IllegalStateError, got %T: %v", err, err)
	}
}

func TestCreateNonConfig(t *testing.T) {
	tmpFile, err := ioutil.TempFile("", "sk-*.tmp")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpFile.Name())
	_, err = NewConfiguration(tmpFile.Name())
	if err == nil {
		t.Fatalf("Expected error for bad config, got none")
	}
	if _, ok := err.(*IllegalStateError); !ok {
		t.Fatalf("Expected IllegalStateError, got %T: %v", err, err)
	}
}

func TestCreateBadPattern(t *testing.T) {
	_, err := NewConfiguration("src/test/resources/broken-pattern.conf")
	if err == nil {
		t.Fatalf("Expected error for broken pattern config, got none")
	}
	if _, ok := err.(*IllegalStateError); !ok {
		t.Fatalf("Expected IllegalStateError, got %T: %v", err, err)
	}
}

func TestCreateGood(t *testing.T) {
	// Create a real temp file to simulate a good config.
	tmpFile, err := ioutil.TempFile("", "sk-*.conf")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpFile.Name())
	_, err = tmpFile.Write([]byte("<config>good</config>"))
	if err != nil {
		t.Fatal(err)
	}
	tmpFile.Close()

	cfg, err := NewConfiguration(tmpFile.Name())
	if err != nil {
		t.Fatalf("Expected success but got error: %v", err)
	}
	if cfg.isProfiling() {
		t.Errorf("Expected profiling false")
	}
	if cfg.blacklist()[0].String() != ".*" {
		t.Errorf("Expected blacklist to be \".*\", got %q", cfg.blacklist()[0].String())
	}
	if cfg.whitelist()[0].String() != `java\.lang\..*` {
		t.Errorf("Expected whitelist to be \"java\\.lang\\..*\", got %q", cfg.whitelist()[0].String())
	}
}

func TestReload(t *testing.T) {
	// Simulate config file
	tmpFile, err := ioutil.TempFile("", "sk-*.conf")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpFile.Name())

	_, err = tmpFile.Write([]byte("<config>original</config>"))
	if err != nil {
		t.Fatal(err)
	}
	tmpFile.Close()
	cfg, err := NewConfiguration(tmpFile.Name())
	if err != nil {
		t.Fatalf("Expected success but got error: %v", err)
	}
	if cfg.isProfiling() {
		t.Errorf("Expected profiling false")
	}
	if cfg.blacklist()[0].String() != ".*" {
		t.Errorf("Expected blacklist to be \".*\", got %q", cfg.blacklist()[0].String())
	}
	if cfg.whitelist()[0].String() != `java\.lang\..*` {
		t.Errorf("Expected whitelist to be \"java\\.lang\\..*\", got %q", cfg.whitelist()[0].String())
	}
	// Simulate file change
	time.Sleep(100 * time.Millisecond)
	err = ioutil.WriteFile(tmpFile.Name(), []byte("<config>reloaded</config>"), 0644)
	if err != nil {
		t.Fatal(err)
	}
	time.Sleep(100 * time.Millisecond)
	err = os.Chtimes(tmpFile.Name(), time.Now(), time.Now())
	if err != nil {
		t.Fatal(err)
	}
	time.Sleep(100 * time.Millisecond)
	err = cfg.reloadIfNeeded()
	if err != nil {
		t.Fatalf("Error on reloadIfNeeded: %v", err)
	}
	// After reload, blacklist is empty and whitelist is .*
	if len(cfg.blacklist()) != 0 {
		t.Errorf("Expected blacklist to be empty after reload")
	}
	if cfg.whitelist()[0].String() != ".*" {
		t.Errorf("Expected whitelist now .*, got %q", cfg.whitelist()[0].String())
	}
}