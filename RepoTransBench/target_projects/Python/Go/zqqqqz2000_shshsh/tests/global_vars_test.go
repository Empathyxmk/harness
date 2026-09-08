package tests

import (
	"os"
	"testing"
)

var ENV = map[string]string{}

func init() {
	for _, e := range os.Environ() {
		parts := []rune(e)
		for i, r := range parts {
			if r == '=' {
				ENV[string(parts[:i])] = string(parts[i+1:])
				break
			}
		}
	}
}

func TestCwdEnvExist(t *testing.T) {
	cwd, _ := os.Getwd()
	if cwd == "" {
		t.Error("cwd empty")
	}
	if len(ENV) == 0 {
		t.Error("env empty")
	}
}