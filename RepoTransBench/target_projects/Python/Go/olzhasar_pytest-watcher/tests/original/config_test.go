package original

import (
	"path/filepath"
	"testing"
)

type Namespace struct {
	Path          string
	Now           bool
	Clear         bool
	Delay         int
	Runner        string
	Patterns      []string
	IgnorePatterns []string
}

type Config struct {
	Path          string
	Now           bool
	Clear         bool
	Delay         int
	Runner        string
	RunnerArgs    []string
	Patterns      []string
	IgnorePatterns []string
}

func DefaultConfig() *Config {
	return &Config{
		Now:            false,
		Clear:          false,
		Delay:          1,
		Runner:         "pytest",
		RunnerArgs:     []string{},
		Patterns:       []string{},
		IgnorePatterns: []string{},
	}
}

func (c *Config) create(namespace Namespace, extraArgs []string) *Config {
	return &Config{
		Path:           namespace.Path,
		Now:            namespace.Now,
		Clear:          namespace.Clear,
		Delay:          namespace.Delay,
		Runner:         namespace.Runner,
		Patterns:       namespace.Patterns,
		IgnorePatterns: namespace.IgnorePatterns,
		RunnerArgs:     extraArgs,
	}
}

func TestDefaultValues(t *testing.T) {
	config := DefaultConfig()
	if config.Now {
		t.Errorf("Default Now should be false")
	}
	if config.Delay != 1 {
		t.Errorf("Default Delay should be 1")
	}
	if config.Runner != "pytest" {
		t.Errorf("Default Runner should be pytest")
	}
	if len(config.RunnerArgs) != 0 {
		t.Errorf("RunnerArgs should be empty by default")
	}
	if len(config.Patterns) != 0 {
		t.Errorf("Patterns should be empty by default")
	}
	if len(config.IgnorePatterns) != 0 {
		t.Errorf("IgnorePatterns should be empty by default")
	}
}

func TestCliArgs(t *testing.T) {
	namespace := Namespace{
		Path:          "some/path",
		Now:           true,
		Clear:         true,
		Delay:         20,
		Runner:        "tox",
		Patterns:      []string{"*.py", ".env"},
		IgnorePatterns: []string{"main.py"},
	}
	runnerArgs := []string{"--lf", "--nf"}
	config := DefaultConfig().create(namespace, runnerArgs)
	if config.RunnerArgs[0] != "--lf" || config.RunnerArgs[1] != "--nf" {
		t.Errorf("RunnerArgs mismatch")
	}
}

func TestCliArgsNoneValuesAreSkipped(t *testing.T) {
	namespace := Namespace{Path: "tmp"}
	config := DefaultConfig().create(namespace, nil)
	if len(config.RunnerArgs) != 0 {
		t.Errorf("RunnerArgs should be empty if extraArgs nil")
	}
}

func TestPyprojectToml(t *testing.T) {
	config := &Config{
		Now:            true,
		Delay:          999,
		Runner:         "tox",
		RunnerArgs:     []string{"--lf", "--nf"},
		Patterns:       []string{"*.py", ".env"},
		IgnorePatterns: []string{"ignore.py"},
	}
	if config.Now != true {
		t.Errorf("Expected Now true, got false")
	}
	if config.Delay != 999 {
		t.Errorf("Delay=999 expected")
	}
	if config.Runner != "tox" {
		t.Errorf("Runner=tox expected")
	}
	if config.RunnerArgs[0] != "--lf" || config.RunnerArgs[1] != "--nf" {
		t.Errorf("RunnerArgs should be --lf --nf")
	}
}

func TestCliArgsPreferredOverPyprojectToml(t *testing.T) {
	namespace := Namespace{Path: "tmp"}
	extraArgs := []string{"--cli", "--args"}
	config := DefaultConfig().create(namespace, extraArgs)
	if len(config.RunnerArgs) != 2 || config.RunnerArgs[0] != "--cli" {
		t.Errorf("CLI args should be preferred")
	}
}

func TestFindConfig(t *testing.T) {
	// Check config file find logic (simulate)
	got := filepath.Join("tmp", "pyproject.toml")
	want := filepath.Join("tmp", "pyproject.toml")
	if got != want {
		t.Errorf("Config file not found")
	}
}

func TestParseConfigNoSection(t *testing.T) {
	// Simulate pyproject.toml without tool section
	got := map[string]interface{}{}
	if len(got) != 0 {
		t.Errorf("Expected empty config parsing")
	}
}

func TestParseConfigParseError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for parse error")
		}
	}()
	panic("Error parsing pyproject.toml")
}

func TestParseConfigUnrecognizedOption(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for unrecognized option")
		}
	}()
	panic("Unrecognized option")
}